# IoT Sensor Temperature Analysis with IBM Db2 Event Store

IBM® Db2 Event Store is an in-memory database designed for massive structured data volumes and real-time analytics built on Apache SPARK and Apache Parquet Data Format. The solution is optimized for event-driven data processing and analysis. It can support emerging applications that are driven by events such as IoT solutions, payments, logistics and web commerce. It is flexible, scalable and can adapt quickly to your changing business needs over time. Available in a free developer edition and an enterprise edition that you can download now. The enterprise edition is free for pre-production and test, please visit the [official product webpage](https://www.ibm.com/products/db2-event-store) for more information.

The sample data used in this code pattern simulates the common data pattern collected by the real industry IoT sensors. The IoT data sample consists of record timestamp, ambient temperature, power consumption, and sensor temperature record by a group of sensors identified with unique sensor IDs and device IDs.

This code pattern contains two parts. The first part demonstrates a simple data load process and the use of a Jupyter notebook to interact with IBM Db2 Event Store, from the creation of the database objects to doing advanced analytics and machine learning model development and deployment. The second part demonstrates advanced usages, including ingesting data using IBM Streams, and running external applications in multiple programming languages and applications.

When the reader has completed this code pattern, they will understand how to:

* Install IBM Db2 Event Store developer edition
* Ingest data into IBM Db2 Event Store
* Interact with Db2 Event Store using Python and a Jupyter notebook
* Perform online scoring using saved machine learning model through curl
* Interact with IBM Db2 Event Store through its REST API
* Run IBM Streams and Remote Access Applications with IBM Db2 Event Store

**Table of Contents**

- [IoT Sensor Temperature Analysis with IBM Db2 Event Store](#iot-sensor-temperature-analysis-with-ibm-db2-event-store)
  * [Abstract](#abstract)
  * [Included components](#included-components)
  * [Featured technologies](#featured-technologies)
  * [Prerequisites](#prerequisites)
- [Workflow](#workflow)
    + [1 . Prepare sample IoT dataset](#1-prepare-the-sample-iot-dataset)
    + [2. Interact with IBM Db2 Event Store using Jupyter notebook](#2-interact-with-ibm-db2-event-store-using-jupyter-notebook)
    + [3. Interact with Event Store database using REST API](#3-interact-with-event-store-database-using-rest-api)
    + [4. Run Example IBM Streams and Remote Access Applications with Event Store](#4-run-example-ibm-streams-and-remote-access-applications-with-event-store)
- [Sample output](#sample-output)
- [Links](#links)
- [Learn more](#learn-more)
- [License](#license)

## Abstract

1. Install IBM Db2 Event Store
2. Setup a Event Store database and table
3. Perform multiple data science tasks with Event Store using Jupyter notebooks
4. Interact with Event Store database using REST API
5. Run example IBM Streams and Remote Access Applications with Event Store

## Included components

* [IBM Db2 Event Store](https://www.ibm.com/us-en/marketplace/db2-event-store): In-memory database optimized for event-driven data processing and analysis.
* [IBM Watson Studio Local](https://www.ibm.com/cloud/watson-studio): Analyze data using RStudio, Jupyter, and Python in a configured, collaborative environment that includes IBM value-adds, such as managed Spark.
* [Jupyter Notebook](http://jupyter.org/): An open source web application that allows you to create and share documents that contain live code, equations, visualizations, and explanatory text.
* [Python](https://www.python.org/): Python is a programming language that lets you work more quickly and integrate your systems more effectively.
* [Java](https://java.com/): A secure, object-oriented programming language for creating applications.
* [Scala](https://www.scala-lang.org/): Scala combines object-oriented and functional programming in one concise, high-level language.

## Featured technologies
* [Databases](https://en.wikipedia.org/wiki/IBM_Information_Management_System#.22Full_Function.22_databases): Repository for storing and managing collections of data.
* [Analytics](https://developer.ibm.com/watson/): Analytics delivers the value of data for the enterprise.
* [Data Science](https://medium.com/ibm-data-science-experience/): Systems and scientific methods to analyze structured and unstructured data in order to extract knowledge and insights.

## Prerequisites

- Install IBM Db2 Event Store Developer Edition or Enterprise Edition

  The IBM Db2 Event Store Enterprise Edition is suggested to be installed in order to execute the examples in this repository. The Enterprise Edition is free for pre-production and test, you are welcomed to visit [official product webpage](https://www.ibm.com/products/db2-event-store) to get the Enterprise Edition for trial.

  * Alternatively you can install the free developer edition on Mac, Linux, or Windows by following the instructions [here. ](https://www.ibm.com/support/knowledgecenter/en/SSGNPV/eventstore/desktop/install.html) However, the function of the developer edition is limited, some tasks cannot be performed with the developer edition.*

  > Note: This code pattern was developed with EventStore-Enterprise Edition 1.1.3

* Clone this github repository to get a local copy of all files

Clone the `db2eventstore-IoT-Analytics` locally. In a terminal, run:

```bash
git clone https://github.com/IBMProjectEventStore/db2eventstore-IoT-Analytics
```

# Workflow

### 1. Prepare the sample IoT dataset

This repository includes a generator to create a  sample IoT dataset in CSV format that contains 1 Million records. The sample CSV dataset can be found at `/data/sample_IOT_table.csv`.

Alternatively, a CSV dataset containing user-specified number of record can be generated with the provided python script at `/data/generator.py`. A Python environment with Pandas and Numpy installed is required to run the script.

```bash
cd data
python ./generator.py -c <Record Count>
```

### 2. Interact with IBM Db2 Event Store using Jupyter notebook

![Architecture](images/architecture.png)

#### a. Load the notebooks in IBM Watson Studio Local

> Note: Db2 Event Store is built with IBM Watson Studio Local

The git repo includes four Jupyter Notebooks which demonstrate interacting with
Db2 Event Store with Spark SQL and multiple popular data science tools.

**Importing the Notebook**

Use the Db2 Event Store / IBM Watson Studio Local UI to create and run the notebook.

1. From the drop down menu (three horizontal lines in the upper left corner), select `My Notebooks`.
2. Click on `add notebooks`.
3. Select the `From File` tab.
4. Provide a name.
5. Click `Choose File` and navigate to the `notebooks` directory in your cloned repo. Select the Jupyter notebook files with name pattern `*.ipynb`.
6. Scroll down and click on `Create Notebook`.
  The new notebook is now open and ready for execution.

#### b. Create IBM Db2 Event Store database and table with Jupyter notebook

Db2 Event Store database and table can be created with one of the Jupyter notebooks provided once it is loaded to the IBM Watson Studio Local. The notebook will drop existing database and create a new database containing a table.

1. Open the Jupyter notebook with name `Event_Store_Table_Creation.ipynb` from Db2 Event Store / IBM Watson Studio Local UI.
2. Edit the `HOST` constant in the first code cell. You will need to enter your host's IP address here.
3. Run the notebook using the menu `Cell > Run all` or run the cells individually with the play button.

#### c. Ingest sample data with the Java Event Store CSV loader

Sample IoT dataset can be ingested to the IBM Db2 Event Store database at lighting speed with Event Store CSV loader. This git repo provides a script that will download the Java CSV loader and ingest the sample CSV dataset into the Event Store database. To run this task, Java 8 must be installed.

```bash
# replace content in < > accordingly

./load.sh --user <user_name> --connstring <host IP>:1101 --filename ./sample_IOT_table.csv --dbname TESTDB --tablename IOT_TEMP --numrowsperbatch 100000
```

When prompted, enter your IBM Db2 Event Store password.

#### d. Run the data analytics notebooks

Run the notebooks below to learn how the IBM Db2 Event Store can be integrated with multiple popular scientific tools to perform various data  analytics tasks.

**`Event_Store_Querying_on_Table.ipynb`**  
This notebook demonstrates best practices for querying the data stored in the IBM Db2 Event Store database. 

**`Event_Store_Data_Analytics.ipynb`**  
This notebook demonstrates performing data analytics on the data stored in the IBM Db2 Event Store database.

**`Event_Store_ML_Model_Deployment.ipynb`**  
This notebook demonstrates building and deploying a machine learning model on the data stored in the IBM Db2 Event Store database. It also shows how to perform online scoring from command line using curl.

**To run each notebook**

1. Open the notebooks from IBM Watson Studio Local UI.
2. Edit the `HOST` constant in the first code cell that is provided as input to the `ConfigurationReader.setConnectionEndpoints()` API. You will need to enter the connection string for your IBM Db2 Event Store deployment.
3. Run the notebook using the menu `Cell > Run all` or run the cells individually with the play button.

### 3. Interact with Event Store database using REST API

The instructions for running the REST API example can be found at: [Event Store REST API instruction](./rest/README.md)

### 4. Run Example IBM Streams and Remote Access Applications with Event Store
![Architecture](images/advanced.png)

The instructions for running the example IBM Streams application and the example remote access applications are here: [Instructions for using IBM Streams and remote access applications with IBM Db2 Event Store](AdvancedApplications/README.md)

# Sample output

See the notebooks with example output here: [notebook examples with result](notebooks_with_result)

# Links
* [**Ingest and Analyze Streaming Event Data at Scale with IBM Db2 EventStore**](http://www.ibmbigdatahub.com/blog/ingest-and-analyze-streaming-event-data-scale-ibm-eventstore)
* [**Fast Data Ingestion, ML Equates to Smarter Decisions Faster**](https://www.ibm.com/blogs/think/2018/03/db2-event-store/)
* [**IBM Db2 Event Store Solution Brief**](https://www-01.ibm.com/common/ssi/cgi-bin/ssialias?htmlfid=09014509USEN&)
* [**Overview of IBM Db2 Event Store Enterprise Edition**](https://www.ibm.com/support/knowledgecenter/en/SSGNPV/eventstore/local/overview.html#overview)
* [**Developer Guide for IBM Db2 Event Store Client APIs**](https://www.ibm.com/support/knowledgecenter/en/SSGNPV/eventstore/desktop/dev-guide.html)
* [**IBM Marketplace**](https://www.ibm.com/us-en/marketplace/db2-event-store)

# Learn more
* **IBM Watson Studio Local**: Master the art of data science with IBM's [IBM Watson Studio Local](https://www.ibm.com/cloud/watson-studio/)

# License
[Apache 2.0](LICENSE)


[@Frank Sun](https://twitter.com/sun_xi_frank), [IBM Db2 Event Store](https://www.ibm.com/products/db2-event-store)

