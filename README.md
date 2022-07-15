# Share Files Securely 📨

_La version française sera disponible bientôt_

This repository is a proof of concept for a secure file sharing service.

https://user-images.githubusercontent.com/867334/176796040-5b054541-201e-402c-b66d-ff40c07ab40a.mp4


## Running in dev container

It is easiest to work with this app in GitHub codespaces as all the env variables a properly pre-populated. Once it is opened in codespaces run: 

```
cd app
make init
make init-dev
make migrate
make serve
```

Make sure you have the temporary AWS credentials for the SRE Tools account otherwise you will not be able to interact with the S3 bucket.