# Load Balancer
**Live Link:** https://load-balancer.osc-fr1.scalingo.io/

**Tech Stack:** Python, Flask, Multiprocessing 
* Developed a load balancer project using **Python** and **Flask**, effectively **distributing** incoming client **requests** to
different **backend servers** using **round-robin algorithm**
* Utilized **multithreading** & **multiprocessing** within the **load balancer** to create a **software-based multi-server
architecture**
* **reduced** the **load** on a single server by **90%** for a 10-server cluster, resulting in **improved performance**

## Video Demo
[![Video Demo](https://img.youtube.com/vi/0aV6pvMUqyE/0.jpg)](https://www.youtube.com/watch?v=0aV6pvMUqyE)

## Here's how I tackled it:

**Flask as the orchestrator:** I built APIs using Flask to handle incoming requests and route them to backend servers.

**Round Robin for load balancing:** I implemented Round Robin load balancing algorithm to distribute incoming requests evenly across the worker processes.

**Multiprocessing for scalability:** I used the multiprocessing module to spawn multiple worker processes, each with its own Flask instance. This allows for parallel processing of requests, effectively distributing the workload.

**Multithreading for responsiveness:** Within each worker process, I leveraged threading to handle multiple concurrent requests within the same process. This ensures smooth and efficient handling of bursts in traffic.

This project was a playground for exploring concurrency, operating systems and system design concepts in Python. I learned a ton, and I'm thrilled with the results!
