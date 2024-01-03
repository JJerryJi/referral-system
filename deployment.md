# Deployment Notes with AWS EKS

## Step 1: setup kubectl
First, you need to have appropriate version of `kubectl`, which is Kubernetes `1.27` in this case.
Also, you need to setup an AWS EKS cluster along with a root user with admin permission. 

When first installing kubectl, it isn't yet configured to communicate with any server.

## Step 2: Setup Config
You need to update the configuration to communicate with a particular cluster, you can run the following command. Replace `region-code` with the AWS Region that your cluster is in. Replace `my-cluster` with the name of your cluster.


```
aws eks update-kubeconfig --region region-code --name my-cluster
```

You can run ``` cat ~/.kube/config ``` to verify if the update-kubeconfig succeed or not. 

## Step 3: SetUp User
Before creating all of the required resources to get started with Amazon EKS, you need to download ```eksctl```.

Also, before getting started, you have to ensure that the current AWS user has the required IAM permission. You can setup the user by `aws configure`, which prompts you to enter AWS `Access Key ID`, `AWS Secret Access Key`, `Default Region Name`, and `Default Output Format`. These information can be retrieved in AWS Console.

Once you set up the user, you can verify the current user by this command. 

```bash
aws sts get-caller-identity
``` 

## Step 4: Create Amazon EKS cluster and nodes
You can create EKS cluster along with nodes by `eksctl`.
You can replace `my-cluster` with your own value, but it must start with an alphabetic character and can't be longer than 100 characters. 
Also, please replace region-code with any AWS Region that is supported by Amazon EKS (for instance, `us-west-1`).

```
eksctl create cluster --name my-cluster --region region-code
```

This command will create a cluster with 2 `M5.large` nodes. The creation process may take several minutes. During creation, you'll see several lines of output in the terminal. The last line of output is similar to be: 

```
[...] 
[✓]  EKS cluster "my-cluster" in "region-code" region is ready
```

Finally, the EKS cluster `my-cluster` will start running after this step. You can verify it either from the AWS Console or using the following command:

```
kubectl get pods -A
kubectl get nodes
```
If you see two nodes/pods running, then it means this step is successful.

Right now, the initial setup is complete. You can start deploying your application to it. 

## Step 5: Sample Deployment (using Port-forward strategy for only local-testing)
You can run the following yaml files in the git repo to setup the `statefulset` and `deployment` resources. 
After that, you can forward the port by 
```
kubectl port-forward 3000:3000
```
```
kubectl port-forward 8088:8000
```
```
kubectl port-forward 8002:8002
```

Then, you can access the React frontend via `http://localhost:3000` and Django Admin Page via `http://localhost:8088/admin`.


## Step 6: Exposing Your Service with an Ingress Resource
You can choose to expose the service using `ingress` resource. Ingress resources are a powerful way to manage access to your services from outside the Kubernetes cluster.

Follow the official [instructions](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html) to setup AWS ALB Ingress Controller.

With the ALB Ingress Controller installed, you can now create an Ingress resource. Here is a sample YAML configuration for an Ingress resource:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
spec:
  ingressClassName: alb
  rules: # define your rules for routing
  - http:
      paths:
      - path: /testpath 
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 8000
```

After applying this yaml file, use the `kubectl get ingress` command to find the URL assigned to your Ingress. And you will be able to access the website via this URL. 

The command output will look something like this:

```
NAME              CLASS   HOSTS   ADDRESS                                                                  PORTS   AGE
example-ingress   alb     *       example-ingress-123456789.us-west-2.elb.amazonaws.com                     80      10m
```

## Step 7: Manage Deployment with Helm (Production)
Helm is a powerful tool for managing Kubernetes applications. All previous yaml files are correctly compiled as templates in `helm` folder.

### Deploying the Chart
Use the command `helm install my-release ./helm` to deploy the chart to your Kubernetes cluster. You can replace `my-release` with your desired release name

### Updating the Deployment
Use the command `helm upgrade my-release ./helm` if you make changes to your chart and need to apply them.

### Rolling back
Use the command `helm rollback my-release` if you want to go back to a previous version in case something goes wrong.

## Notes 
### Common Problem 1: CSI driver add-on setup for Storage Class 
For the use case that requires persistent storage (i.e., in `statefulset`, you use `volumeClaimTemplates` and `volumeMounts`), we need to configure `CSI driver` add-on through `eksctl`  for the default `pg2` storage class.

Run this command to verify the availability of `pg2`:
```kubectl get sc```

If you run ```kubectl get pvc```, and it will display `failed to provision volume with StorageClass` along with a `could not create volume in EC2: UnauthorizedOperation` error. You must complete this additional step. (For the first time you setup the cluster, you are unlikely skip this step.)

----
#### Additional Step: Creating an IAM OIDC provider for your cluster
You can easily create an IAM OIDC identity provider for your cluster with `eksctl`.
Just run the following command in sequence: 

```
cluster_name=my-cluster
```

```
oidc_id=$(aws eks describe-cluster --name $cluster_name --query "cluster.identity.oidc.issuer" --output text | cut -d '/' -f 5)
echo $oidc_id
```

```
eksctl utils associate-iam-oidc-provider --region=YourClusterRegion --cluster=YourClusterNameHere --approve
```

If the OIDC provider is setup correctly, this will display a number: 

```
aws iam list-open-id-connect-providers | grep $oidc_id | cut -d "/" -f4
```

After that, you can continue with next step. You can also refer this link.

[Link to StackOverflow Question](https://stackoverflow.com/questions/75758115/persistentvolumeclaim-is-stuck-waiting-for-a-volume-to-be-created-either-by-ex)

[Link to AWS OIDC Provider Doc](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)

[Link to AWS EBS CSI driver Doc](https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html#adding-ebs-csi-eks-add-on)

-----
#### How to create the Amazon EBS CSI driver IAM role?
Replace my-cluster with the name of your cluster, and run the following command. 
``` bash
eksctl create iamserviceaccount \
    --name ebs-csi-controller-sa \
    --namespace kube-system \
    --cluster my-cluster \
    --role-name AmazonEKS_EBS_CSI_DriverRole \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
    --approve
```
The command deploys an AWS CloudFormation stack that creates an IAM role and attaches the IAM policy to it. If your cluster is in the AWS GovCloud (US-East) or AWS GovCloud (US-West) AWS Regions, then replace arn:aws: with arn:aws-us-gov.

-----
If this command fails, you can delete `iamserviceaccount` that was just created and then reapply the above command.

Then, the `CSI Driver` should be correctly setup and if you run `kubectl get pvc`. You shall see all pvc are in `Bound` status.

### Common Problem 2: exec exec xxx.sh: exec format error
This error is likely due to the docker image pulled from the DockerHub does not support AWS EKS Linux Machine. To fix it, you need to find the official image from DockerHub that support amd64-linux. 

Or if the image is built locally, you can specify target platform using `--platform` in `docker buildx build` command. For instance, `docker buildx build --platform linux/amd64 -t [USERNAME]/[REPOSITORY_NAME]:[TAG] . --push`