# Author
Zhunaid Mohamed

# Revision 1 Updates
- [x] Use DB Migration files that can be PR'd.
- [x] Improve naming conventions to be more consistent, i.e., use "Id" instead of "ID."
- [x] Use Django forms for filtering views.
- [x] Use Text field for model fields with very large lengths.
- [x] Create Email template model.
- [x] Implement email blurb construction.
- [x] Setup Email Backend to print to console.
- [x] Ensure that validation checks follow fail-fast by checking base cases.
- [x] Investigate using get_object_or_404 (Removed due to not being consistent with the rest of the view/model approach).
- [x] Ensure that all get functions on models have a try/except for when the entry does not exist.
- [x] Update preesigned_url to be more descriptive.
- [x] Dynamically build out upload and download URLs using request information.
- [x] Use a base model and inherit for created_at.
- [x] Update Model on_delete for foreign keys to SET_NULL where data retention would be necessary.
- [x] Updated all Enums to use Django Integer choices for consistency.
- [x] Switch upload_id to text to allow easy changing and not being locked to UUID.
- [x] Streamlined logic to check whether an upload_id is valid in utilities.
- [x] Research Fat Model / Skinny view vs. Skinny Model / Fat View (The approach in this project is Skinny Models to separate the business and data access logic).
- [x] Create a form for Document Creation requests that is reused by the Documents and Customers View.
- [x] Some general code cleanup and updates to ensure consistency in the project.

# Project setup

## Installation
- pip install django

## DB Migration
- python manage.py migrate
- python manage.py loaddata seed.json

## Run server
- python manage.py runserver

## Visit Web app
Navigate to 127.0.0.1:8000/ on your web browser

# Pull Request change to Model
- If you have made a change to a model run `python manage.py makemigrations` and pull request the newly created migration file.

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
- Create Document Requests for a customer
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
- An email will be constructed from the template matching the document type and sent to the customer
    - The EmailBackend is set to console so the sent email will be printed.
- If the status is completed such that the customer has completed the upload, the document can be downloaded with the download button

## Customer upload file
- The `Upload URL` will navigate to a one-time use link to upload a file which will link to that document request
    - This should be handled by Apache tools in the future to handle size_limits, virus and magic bytes scans. But for now any attachment is allowed
- The Link has some limitations
    - You can only upload once
    - It expires after a week
    - Since there is no customer authentication, if this link is leaked somebody could potentially upload a file using this link. This can be a security concern but for this usecase we have no form of customer auth so this is okay.

## Download a Customer uploaded file
- Once the customer has uploaded their file the corresponding document requests will have a download option.

# Future State

- The UI/UX Experience could be better improved by using a proper UI library like Bootstrap.
- Currently the HTML and CSS is basic using simple lists it could be improved long term.
- When a Document request is created an email with generated insructions and url is sent to the console backend. In production this should be switched with an SMTP server or email service such as SES
   -  The email templates are currently set but a possible feature could be to allow the RM to change the template before sending it to the customer.
- There is currently no pagination so when the data scales it should be introduced in UI and DB calls.
- The RM is hardcoded to 1 for some API Calls since we don't have authetication and context of the currently logged in RM.
- The Document upload with pre-signed url should be handled by something like s3 presigned urls in Production.
- When creating a Document Request through the Customers tab the page reloads which resets the expanded customer. This experience could be improved by keeping the customer expanded to immediately see the update