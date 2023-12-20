# News parser

## Summary
This small app parses the https://news.am/eng/ site, saves the latest news in a database, and then displays the latest news on a Vue3 page."


## Prerequisites

- Docker: Ensure you have Docker installed on your system.

## Config

* You can config your parser in `сonfig.yaml`
  For example, you can change the parse interval.

## Setup

To setup the application, follow these steps:

### Clone the Repository

* Clone the repository to your machine:

```bash
git clone https://github.com/SVerstov/genAI_masters_task
cd genAI_masters_task
```

* Buld an aplication:

```
docker-compose build
```

* This process may take some time, so feel free to grab a coffee while you wait!

* To start the application, use:

```
* docker-compose up
```

* By default, app will start on 8008 port!

* Have a nice day!