# Publishing notes

Use these commands from the VM that contains the finished Labtainer lab.

## Docker Hub

```bash
docker tag vp9-parity-coeff-stego.sender.student:latest DOCKERHUB_USERNAME/vp9-parity-coeff-stego-sender:latest
docker tag vp9-parity-coeff-stego.analyst.student:latest DOCKERHUB_USERNAME/vp9-parity-coeff-stego-analyst:latest

docker push DOCKERHUB_USERNAME/vp9-parity-coeff-stego-sender:latest
docker push DOCKERHUB_USERNAME/vp9-parity-coeff-stego-analyst:latest
```

## GitHub

```bash
git init
git add .
git commit -m "Add VP9 directed parity coefficient stego Labtainer lab"
git branch -M main
git remote add origin GITHUB_REPOSITORY_URL
git push -u origin main
```

