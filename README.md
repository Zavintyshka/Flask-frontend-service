# Flask Frontend

This project serves as the frontend for the `MediaConverterApp`, an application that processes various types of media files, including:

- Video files;
- Image files;
- Audio files.

`MediaConverterApp` is built using a microservice architecture, which makes it easy to scale. For instance, adding a new frontend application like a Telegram bot or introducing a new backend service for processing additional file types is straightforward.

---

# Overall Structure

The application follows a microservice architecture where components communicate using different protocols:
<img width="1517" alt="general_scheme" src="https://github.com/user-attachments/assets/11a9ae4e-d12e-4e03-8cdd-e9b4f355da81">

- All client requests from the frontend are forwarded to the API Gateway via HTTP, where further actions are performed.
- Microservices communicate with the API Gateway using gRPC.

---

# Features

## User Accounts

`MediaConverterApp` allows users to create accounts, enabling them to process files at any time. All processed files are stored on the user’s files page, making it easy to download previously converted files. The app also features an achievement system to track user progress. Additionally, users can reset their passwords by receiving reset instructions via email.

![user_profile_preview](https://github.com/user-attachments/assets/7413e90d-ed06-4447-976c-73acb90d07c4)

## User Files

All processed files are displayed in an accessible layout, allowing users to revisit and download older files.
<img width="1090" alt="user_files" src="https://github.com/user-attachments/assets/1caf73e1-617f-4daf-ba81-4c51cd2bbdcf">

## Achievements

The achievement system offers tasks for users to complete, unlocking new cards.
<img width="1090" alt="achievements" src="https://github.com/user-attachments/assets/2c5f5b32-32fb-4954-8074-a8c7e0bbf965">

## Application Status

The app also features a status page displaying the current state of various services:
<img width="1082" alt="status_page" src="https://github.com/user-attachments/assets/3a019282-aee5-4bd1-b16e-a62c7b8397c5">

## Video Service

Allows users to cut and convert video files into different formats:
<img width="1065" alt="video_service" src="https://github.com/user-attachments/assets/176b00c7-c54d-46dd-a531-cec90d0d5a43">

---

# Application Pages

Most of the pages support responsive layouts, making the application accessible on mobile devices:
<img alt="IMG_8129" height="700" src="https://github.com/user-attachments/assets/ecc72f43-c4a8-4f4c-b664-cb7541712adc"/>

## Index

The home page features a parallax effect.
(Screenshot taken from the game Resident Evil 2, location - Main Hall)

![index_preview](https://github.com/user-attachments/assets/d93664ba-8edf-4902-9a7a-612c8f89a069)

## About

![about_preview_compressed](https://github.com/user-attachments/assets/fdc6e67f-f2f3-41db-b722-9a67e5178ccf)
