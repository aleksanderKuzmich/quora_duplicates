# quora_duplicates

Create image:
```bash
docker build --no-cache --tag quora-duplicates .
```
Run container
```bash
# Prepare dir
mkdir /home/alex/Documents/studia/sem_VIII/AJiO/testing/container_output

# set cron schedule - every Sunday at 01:00 AM
0 1 * * SAT /home/alex/Documents/studia/sem_VIII/AJiO/quora_duplicates/runner.sh >> /home/alex/Documents/studia/sem_VIII/AJiO/testing/run.log 2>&1
```