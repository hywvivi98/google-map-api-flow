# google-map-api-flow

## Prerequisite

In order to run this project, you need to have:

- Google Map API Key: to be able to retrieve data from the text search API call
- AWS Account and with attached IAM policies to be able to get access to S3 resources

## How to Run This Project?

1. Start Docker locally, make sure your Docker Desktop is running

2. Pull the image from the Docker hub with the following code

```
docker pull hellovivvvv/google-map-api:latest
```

3. Run the container in the interactive mode because we included input selectors in the code

```
docker run -it hellovivvvv/google-map-api:latest
```

4. While the container is running, provide the information including

- Search Query
- Google map API key
- The lowest restaurant rating you could accept
- The maximal number of result you want to get
- Desired AWS S3 bucket name
- AWS account region name
- AWS access key id
- AWS secret access key

5. After that, you're ready to have a preview of the results in your terminal, and you can get the data in csv format from your S3 bucket


## Something Else?
I also wrote a Medium blog with some interesting stories about this mini-project, welcome to take a look and drop any comments! Link here: https://medium.com/@yh3406/how-to-convince-your-data-eng-manager-not-having-sweetgreen-all-the-time-d415b2d59be9
