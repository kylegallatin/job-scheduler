## Base Image for Python Applications
This repo contains the base image for our Pyrhon applications. It could serve as the base for dash, flask, streamlit, or other Python-based apps.

### Release a new image
1. Bump the minor version (`TAG_NAME`) in `cloudbuild.yaml`
1. Merge the PR to main
1. Check the cloudbuild history to see the build progress

A build trigger in Google Cloud build will build and release a new version of the image:
```
gcr.io/serene-radius-314018/python/python-base:$VERSION
```
To see the manual release process, check out `release.sh`. To ensure this image is used in prod, update the image version for the corresponding yaml in the website directory.

### Test locally
To test locally, you can add commands to the Dockerfile and run tests by copying Python applications in the image, and running the application with the proper port exposed (default 5000 for flask, 8050 for dash, etc). You may have to add lines to the Dockerfile to copy the app to the proper location.

```bash
docker build -t python-app-test .
docker run -p 5000:5000 -it rshiny-app-test
```