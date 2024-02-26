# Batch Processing with Spark on GCP VM Instance
## GCP VM Instance
1. Generate SSH Key and Add to Project Metadata
    Generate SSH key on a local machine.
    ```bash
    ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
    ```

    Print the public key.
    ```bash
    cat ~/.ssh/KEY_FILENAME.pub
    ```

    Add the public key to the project metadata.\
        Go to **Compute Engine -> Metadata** and click on **SSH Keys**. Add the public key to the list.

2. Create VM Instance

    Go to **Compute Engine -> VM Instances** and click on **Create Instance**.

    1. Fill in the name.
    2. Select a region and zone near you.
    3. Select the machine type as **e2-standard-4(4 vCPU, 2 core, 16 GB memory)**
    4. Select the boot disk's operating system as **Ubuntu 20.04 LTS**, disk type as **SSD persistent disk**, and size up to **30 GB**.
    5. Select **Allow HTTP traffic** and **Allow HTTPS traffic** in Firewall.
    6. Click on **Create**.
    
<!-- 3. Setup Firewall Rules

    Go to **VPC Network -> Firewall** and click on **Create Firewall Rule**.

    1. Fill in the name. (e.g jupyter-notebook)
    2. Select **All instances in the network** in **Targets**.
    3. Select **IPv4 ranges**.
    4. Fill in the IP range as **0.0.0.0/0**
    5. Select **tcp** and enter **port number** in **Protocols and ports**. -->

3. Setup `~/.ssh/config` file on local machine
    ```bash
    vim ~/.ssh/config
    ```
    Add the following lines to the file and save it with `Esc` + `:wq`.
    ```bash
    Host GCP_VM_INSTANCE_NAME
        HostName EXTERNAL_IP_ADDRESS
        User USERNAME
        IdentityFile ~/.ssh/KEY_FILENAME
    ``` 

4. Connect to VM Instance
    ```bash
    ssh GCP_VM_INSTANCE_NAME
    ```
    Type `yes` if it is the first time connecting to the instance.

5. Install **Remote SSH** extension in VSCode and connect to the VM instance

    Press `command` + `shift` + `p` and type `Remote-SSH: Connect to Host...`. Select the host `GCP_VM_INSTANCE_NAME` from the list and connect to the VM instance.

    Select `New Terminal` in VSCode.

## Jupyter Notebook
1. Update and Upgrade resources
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
2. Install Anaconda
    
    Download the latest version of Anaconda from the [official website](https://www.anaconda.com/download#downloads).
    ```bash
    wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
    ```

    Run the installer and keep typing `yes`.
    ```bash
    bash Anaconda3-2023.09-0-Linux-x86_64.sh
    ```
    
    Activate the changes.
    ```bash
    source ~/.bashrc
    ```

    Make a `notebook` directory and change the current directory.
    ```bash
    mkdir notebook
    cd notebook
    ```

    Launch the Jupyter Notebook and forward the port to the local machine in VSCode.
    ```bash
    jupyter notebook --port=5000 --no-browser
    ```

## Spark
1. Make a directory for Spark and change the current directory.

    ```bash
    mkdir spark
    cd spark
    ```

2. Install Java

    Download and install the `11.0.2` version of Java on [official website](https://jdk.java.net/archive/).
    ```bash
    wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
    ```
    Unzip the file.
    ```bash
    tar zxfv openjdk-11.0.2_linux-x64_bin.tar.gz
    ```

    Add the path to the `~/.bashrc` file via `vim ~/.bashrc` and restart the bash with `source ~/.bashrc`.
    ```bash
    export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
    export PATH="${JAVA_HOME}/bin:${PATH}"
    ```

    Check the Java version.
    ```bash
    java --version
    ```

    Remove the downloaded file.
    ```bash
    rm openjdk-11.0.2_linux-x64_bin.tar.gz
    ```

3. Install Spark

    Go to the [official website](https://spark.apache.org/downloads.html) and download the latest version of Spark. We choose version `3.4.2` and package type `Pre-built for Apache Hadoop 3.3 and later`. And then click the link in `Download Spark` to direct to the mirror link.

    ```bash
    wget https://dlcdn.apache.org/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz
    ```

    Unzip the file.
    ```bash
    tar zxfv spark-3.4.2-bin-hadoop3.tgz
    ```

    Add the path to the `~/.bashrc` file via `vim ~/.bashrc` and restart the bash with `source ~/.bashrc`.

    ```bash
    export SPARK_HOME="${HOME}/spark/spark-3.4.2-bin-hadoop3"
    export PATH="${SPARK_HOME}/bin:${PATH}"
    ```

    Run `spark-shell` to check if the installation is successful.
    ```scala
    val data = 10 to 1000
    ```

## PySpark
1. Export PySpark path to the `~/.bashrc` file via `vim ~/.bashrc` and restart the bash with `source ~/.bashrc`.

    ```bash
    export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
    export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH"
    ```

2. Change directory to the `notebooks` and check if we can import PySpark properly.

    ```bash
    cd ~/notebook
    jupyter notebook
    ```

    Download test data.
    ```bash
    wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
    ```

    Create a new notebook and type the following code.

    ```python
    import pyspark
    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .getOrCreate()

    df = spark.read \
        .option("header", "true") \
        .csv('taxi+_zone_lookup.csv')

    df.show()

    df.write.parquet('zones')
    ```

    If there is no error, the installation is successful.
