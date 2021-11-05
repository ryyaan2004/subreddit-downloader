# subreddit-downloader
A very simple set of functions to download subreddit submissions using the [pushshift.io api](https://pushshift.io). Provides a simple cli and docker image as well


## using docker
The entrypoint has been set as the script, so just pass flags after the image name to configure. The image also creates a `/out` dir within the container to serve as the output path that can be mounted to for ease of use. Putting it all together looks like `docker run --rm -v $(pwd)/your/dir:/out downloader:latest -f /out/your-file.json`
