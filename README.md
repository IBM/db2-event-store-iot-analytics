# IoT sensor temperature analysis and prediction with IBM Db2 Event Store

This code pattern demonstrates the use of a Jupyter notebooks to interact with IBM Db2 Event Store -- from the creation of database objects to advanced analytics and machine learning model development and deployment.

The sample data used in this code pattern simulates data collected by real industry IoT sensors. The IoT sample data includes sensor temperature, ambient temperature, power consumption, and timestamp for a group of sensors identified with unique sensor IDs and device IDs.

Db2 Event Store is an in-memory database designed for massive structured data volumes and real-time analytics built on Apache Spark and Apache Parquet Data Format. The solution is optimized for event-driven data processing and analysis. It can support emerging applications that are driven by events such as IoT solutions, payments, logistics and web commerce. It is flexible, scalable and can adapt quickly to your changing business needs over time. Db2 Event Store is available in a free developer edition and an enterprise edition that you can download now. The enterprise edition is free for pre-production and test, please visit the [official product webpage](https://www.ibm.com/products/db2-event-store) for more information.

> Note: Db2 Event Store is built with IBM Watson Studio

After completing this code pattern, you’ll understand how to:

* Interact with Db2 Event Store using Python and a Jupyter notebook
* Use IBM Streams to feed data into Db2 Event Store
* Visualize data using Matplotlib charts
* Build and test a machine learning model
* Deploy and use the model with Watson Machine Learning

![architecture](doc/source/images/architecture.png)

## Flow

1. Create the Db2 Event Store database and table
2. Feed the sample IoT dataset into Db2 Event Store
3. Query the table using Spark SQL
4. Analyze the data with Matplotlib charts
5. Create and deploy a machine learning model

## Steps

1. [Clone the repo](#1-clone-the-repo)
2. [Install the prerequisites](#2-install-the-prerequisites)
3. [Create an IBM Db2 Event Store database and table](#3-create-an-ibm-db2-event-store-database-and-table)
4. [Add the sample IoT data](#4-add-the-sample-iot-data)
5. [Query the table](#5-query-the-table)
6. [Analyze the data](#6-analyze-the-data)
7. [Create and deploy a machine learning model](#7-create-and-deploy-a-machine-learning-model)

### 1. Clone the repo

Clone the `db2-event-store-iot-analytics` repo locally. In a terminal, run:

```bash
git clone https://github.com/IBM/db2-event-store-iot-analytics
```

### 2. Install the prerequisites

#### Install Event Store

> Note: This code pattern was developed with EventStore-DeveloperEdition 1.1.4

1. Install IBM® Db2® Event Store Developer Edition on Mac, Linux, or Windows by following the instructions [here.](https://www.ibm.com/products/db2-event-store)

#### Install IBM Streams

> Note: This is optional if you prefer to use the provided Jupyter notebook to load the data.

1. Install the Quick Start Edition(QSE) Docker image for IBM Streams 4.3.1 by following the instructions [here](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.qse.doc/doc/qse-docker.html).

1. Download the toolkit for Event Store Developer Edition 1.1.4 [here](https://github.com/IBMStreams/streamsx.eventstore/releases/tag/v1.2.0-Developer-v1.1.4).

1. Extract the contents of the toolkit. For example, you can make a `toolkits` directory in the hostdir that you mapped to a local dir when installing the Quick Start Edition and extract the files into that directory.

   ```bash
   mkdir $HOME/hostdir/toolkits
   tar -zxvf  streamsx.eventstore_1.2.0-RELEASE.tgz -C $HOME/hostdir/toolkits/
   ```

### 3. Create an IBM Db2 Event Store database and table

The Db2 Event Store database and table can be created with one of the Jupyter notebooks provided. Refer to the notebook comments if you need to drop your existing database or table.

Use the Db2 Event Store UI to create and run a notebook as follows:

1. From the upper-left corner `☰` drop down menu, select `My Notebooks`.
1. Click on `add notebooks`.
1. Select the `From File` tab.
1. Provide a name.
1. Click `Choose File` and navigate to the `notebooks` directory in your cloned repo. Open the Jupyter notebook file named **`Event_Store_Table_Creation.ipynb`**.
1. Scroll down and click on `Create Notebook`.
1. Edit the `HOST` constant in the first code cell. You will need to enter your host's IP address here.
1. Run the notebook using the menu `Cell ▷ Run all` or run the cells individually with the play button.

### 4. Add the sample IoT data

#### Generate the data

This repository includes a generated sample IoT dataset in CSV format that contains 1 million records. The sample CSV dataset can be found at `data/sample_IOT_table.csv`.

Alternatively, a CSV dataset containing a user-specified number of records can be generated with the provided Python script at `data/generator.py`. A Python environment with pandas and NumPy installed is required to run the script.

```bash
cd db2-event-store-iot-analytics/data
python ./generator.py -c <Record Count>
```

#### Stream the data into Event Store

If you have installed IBM Streams, use a streams flow to feed the sample data into Event Store. Otherwise, a data feed notebook has been provided as a shortcut.

Click to expand the data feed instructions for IBM Streams or for the Jupyter notebook. Choose one:

<details><summary>Use an IBM Streams flow</summary>
<p>

1. Use VNC to connect to your IBM Streams QSE at vnc://streamsqse.localdomain:5905

   > **Tip:** On macOS, you can use Finder's menu: `Go ▷ Connect to Server...` and connect to `vnc://streamsqse.localdomain:5905`, and then in your session use `Applications ▷ System Tools ▷ Settings ▷ Devices ▷ Displays` to set the display `Resolution` to `1280 x 1024 (5:4)`.

   ![connect_to_server.png](doc/source/images/connect_to_server.png)

1. Launch Streams Studio

   ![streams_studio.png](doc/source/images/streams_studio.png)

1. Create a new project

   - [ ] Select a workspace

   - [ ] If prompted to "Add Streams Domain connection", use the `Find domain...` button to select `streamsqse.localdomain`.

   - [ ] Use the upper-left pulldown to create a new project. When prompted to `Select a wizard`, use `IBM Streams Studio ▷ SPL Project`, hit `Next`, provide a name, and hit `Finish`.

1. Replace the Event Store toolkit

   - [ ] Using the `Project Explorer` tab, expand your new project, right-click on `Dependencies` and select `Edit Dependencies`. Remove `com.ibm.streamsx.eventstore` version 2.0.3. This is a newer version that does not work with our 1.1.4 Developer Edition of Event Store.

   - [ ] Using the `Streams Explorer` tab, expand `IBM Streams Installations` and `IBM Streams` to show `Toolkit Locations`. Right-click and select `Add Toolkit Location...`. Use the `Directory...` button and add the `/home/streamsadmin/hostdir/toolkits` directory (where you extracted the the streamsx.eventstore_1.2.0-RELEASE.tgz toolkit).

   - [ ] Back in the `Project Explorer` tab, right-click on `Dependencies` and select `Edit Dependencies`, `Add`, and `Browse`. Select `com.ibm.streamsx.eventstore 1.2.0` and hit `OK`. Now we are using the downloaded version that works with our 1.1.4 Developer Edition and ignoring the newer version.

     ![add_toolkit_location.png](doc/source/images/add_toolkit_location.png)

1. Create your file source

   - [ ] Copy the `data/sample_IOT_table.csv` file from your cloned repo to your hostdir.

   - [ ] In the `Project Explorer` tab, right-click on your project and select `New  ▷ Main Composite` and create a default `Main.spl`.

     ![main_composite.png](doc/source/images/main_composite.png)

   - [ ] Using the SPL Graphical Editor for `Main.spl`, drag-and-drop the `Toolkits ▷ spl ▷ spl.adapter ▷ FileSource ▷ FileSource` into the `Main` box.

     ![file_source.png](doc/source/images/file_source.png)

   - [ ] Double-click the FileSource box, select `Param` in the left sidebar, and edit the value to set it to `"/users/streamsadmin/hostdir/sample_IOT_table.csv"` (where you put the data file). Add a `format` parameter and set the value to `csv`.

     ![file_source_params.png](doc/source/images/file_source_params.png)

   - [ ] Select `Output Ports` in the left sidebar. Remove the `<extends>` row. Click on `Add attribute...`. Add attributes and types to create an output stream schema matching the contents of the CSV file and the Event Store table. The attribute names here don't matter, but the types do. Follow the example below.

     ![output_stream_schema.png](doc/source/images/output_stream_schema.png)

   - [ ] Close and save the FileSource properties.

1. Create your Event Store Sink

   - [ ] Using the SPL Graphical Editor for `Main.spl`, drag-and-drop the `Toolkits ▷ com.ibm.streamx.eventstore ▷ com.ibm.streamx.eventstore ▷ EventStoreSink` into the `Main` box (be sure to grab the 1.2.0 version).

   - [ ] Use your mouse and drag from FileSource output tab to the EventStoreSink input tab.

     ![connected.png](doc/source/images/connected.png)

   - [ ] Double-click the EventStoreSink box, select `Param` in the left sidebar, and edit the values to set the connectionString, databaseName and tableName as shown below (but substitute your own Event Store IP address). Close and save.

     ![event_store_params.png](doc/source/images/event_store_params.png)

1. Launch

   - [ ] Save all your changes and let the build finish.

   - [ ] Right-click on your application (`Main`) and `Launch ▷ Launch Active Build Config as Standalone`.

     ![launch_standalone.png](doc/source/images/launch_standalone.png)

</p>
</details>

<details><summary>Use the Jupyter notebook to load the data</summary>
<p>

Use the Db2 Event Store UI to add the CSV input file as a data asset.

1. From the upper-left corner `☰` drop down menu, select `My Notebooks`.

   ![go_to_my_notebooks](doc/source/images/go_to_my_notebooks.png)

1. Scroll down and click on `add data assets`.

   ![add_to_my_notebooks](doc/source/images/add_to_my_notebooks.png)

1. Click `browse` and navigate to the `data` directory in your cloned repo. Open the file `sample_IOT_table.csv`.

   ![data_assets](doc/source/images/data_assets.png)

Follow the same process as above to add and run a notebook. This time choose the file named **`Event_Store_Data_Feed.ipynb`**.

The notebook loads the table with one million records from the CSV file that you added as a project asset.

</p>
</details>

### 5. Query the table

Follow the same process to add and run a notebook. This time choose the file named **`Event_Store_Querying.ipynb`**.

This notebook demonstrates best practices for querying the data stored in the IBM Db2 Event Store database. Verify that you have successfully created and loaded the table before continuing.

### 6. Analyze the data

Next, run the data analytics notebook. Use the file **`Event_Store_Data_Analytics.ipynb`**.

This notebook shows how the IBM Db2 Event Store can be integrated with multiple popular scientific tools to perform various data analytics tasks. As you walk through the notebook, you'll explore the data to filter it and example the correlation and covariance of the measurements. You'll also use some charts to visualize the data.

#### Probability plots, box plots, and histograms for temperature data

![plots](doc/source/images/plots.png)

#### Scatter plots to show the relationship between measurements

![scatters](doc/source/images/scatters.png)

### 7. Create and deploy a machine learning model

This section demonstrates building and deploying a machine learning model. The notebook uses Spark MLlib to build and test a prediction model from our IoT temperature sensor data. At the end, it demonstrates how to deploy and use the model.

If you are using the **Enterprise Edition** of Db2 Event Store, the notebook will deploy the model using Db2 Event Store which is built with Watson Studio Local.

If you are using the **Developer Edition** of Db2 Event Store, you need an IBM Cloud Watson Machine Learning service instance to complete the deployment. Follow these steps:

* Sign in and create the service [here](https://cloud.ibm.com/catalog/services/machine-learning).
* Click on `Service credentials` and then `New credential` and `Add`.
* Use `View credentials` and copy the credentials JSON.
* You will use the JSON to set the `wml_credentials` variable in the notebook.
* The notebook will pip install watson-machine-learning-client. After the install, you usually need to restart your kernel and run the notebook again from the top.

Load the notebook, using the file **`Event_Store_ML_Model_Deployment.ipynb`**.

Once the model is built and deployed, you can easily send it a new measurement and get a predicted temperature (one at a time or in batches).

#### Given a new data point

```python
new_data = {"deviceID" : 2, "sensorID": 24, "ts": 1541430459386, "ambient_temp": 30, "power": 10}
```

#### The result includes a predicted temperature

```python
predictions:  [48.98055760884435]
```

## Sample output

See all the notebooks with example output [here](examples).

## License

This code pattern is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
