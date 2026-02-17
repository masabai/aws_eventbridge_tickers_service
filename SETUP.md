**Step 1:** Create the "Packing List" (Dockerfile)
In the same folder where your asset.py and mfunds_ses.py
create a new file named exactly Dockerfile (no file extension).

**Step 2:** Build the Image (Creating the "Box")
docker build -t financial-monitor:latest .

**Step 3.** Load the Keys (The Vault)
kubectl apply -f secrets.yaml

**Step 4.** Trigger the Manual Test (The "Run Now")
kubectl delete job manual-test-run --ignore-not-found
kubectl create job --from=cronjob/financial-monitor-job manual-test-run
kubectl logs -l job-name=manual-test-run -f

**Step 5.** Set the Timer (The Schedule)
kubectl apply -f cronjob.yaml

**Step 6.** Cleanup (Save RAM)
kubectl delete cronjob financial-monitor-job
kubectl delete job manual-test-run
