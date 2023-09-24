# Author
Zhunaid Mohamed

# Project setup

## Installation
- pip install django

## DB Migration
- python manage.py makemigrations 
- python manage.py migrate
- python manage.py loaddata seed.json

## Run server
- python manage.py runserver

## Visit Web app
Navigate to 127.0.0.1:8000/ on your web browser

# Flow of application

## Viewing Customers
#### On the customers tab you can
- View each customer assigned to you as a RM
- Filter by name or email
- View each customers documents
- Create Docuement Requests for a customer
- View the generated URL for customer upload
- Download the file if the customer has completed the upload.

## Viewing Documents
#### On the documents tab you can
- View each document request for customers assigned to you
- Filter by customer, status of document request and order by the created at field
- Create Docuement Requests for a customer
- View the generated URL for customer upload
- Download the file if the customer has completed the upload.

## Viewing Notifications
### On the notifications tab you can
- Filter by read and unread notifications and order by the created at field
- You can mark individual notifications as read or click a button to mark all.
- Unread notifications will be highlighted in grey.
- The title of the notifications tab will show the number of new notifications that are not marked as read
    - For now it is just when a customer completes a Document Request

## Creating a Document Request
- A document request can be generated through the customer in the customers tab or on the Documents Tab
- You provde the name of the Document request and the type of document you are requesting
   - The full feature should send an email to the customer with the revelant instructions and the presigned url to upload the file
- A presigned URL is generated under `Upload URL` for a link to the customer to upload the file
- If the status is completed such that the customer has completed the upload, the document can be downloaded with the download button

## Customer upload file
- The `Upload URL` will navigate to a one-time use link to upload a file which will link to that document request
    - This should be handled by Apache tools in the future to handle size_limits, virus and magic button scans. But for now any attachment is allowed
- The Link has some limitations
    - You can only upload once
    - It expires after a week
    - Since there is no customer authentication, is this link is leaked somebody could potentially upload a file using this link. This can be a security concern but for this usecase we have no form of customer auth so this is okay/

## Download a Customer uploaded file
- Once the customer has uploaded their file the corresponding document requests will have a download option.

# Future State

- The UI/UX Experience could be better improved by using a proper UI library like Bootstrap.
- Currently the HTML and CSS is basic using simple lists it could be improved long term.
- When a Document request is created an email with generated insructions and pre-signed url should be sent to Customer using a Email Service like AWS SES
   -  The email blurbs could be set or allowed to be altered by the RM to tailor to specific customers.
- There is currently no pagination so when the data scales it should be introduced in UI and DB calls.
- The RM is hardcoded to 1 for some API Calls since we don't have authetication and context of the currently logged in RM.
- The Document upload with pre-signed url should be handled by something like s3 presigned urls in Production.
- When filtering on one of the views the values of the filters don't show in the filter boxes when a reload/filter is complete. Can be improved by keeping track of filters
- When creating a Document Request through the Customers tab the page reloads which resets the expanded customer. This experience could be improved by keeping the customer expanded to immediately see the update