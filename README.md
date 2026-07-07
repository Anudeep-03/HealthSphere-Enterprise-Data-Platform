# HealthSphere Enterprise Data Platform

HealthSphere Enterprise Data Platform is a production-inspired healthcare data engineering project that demonstrates how modern healthcare organizations can collect, process, validate, and analyze patient events using an event-driven architecture.

The platform simulates a real-world healthcare ecosystem where operational microservices generate patient-related events that are streamed through Apache Kafka, processed using Apache Spark Structured Streaming, stored in a Medallion Architecture (Bronze, Silver, and Gold) powered by Delta Lake, validated with Great Expectations, and prepared for analytics and business intelligence.

The project follows enterprise software engineering practices, including Docker-based containerization, reusable shared libraries, modular microservices, orchestration-ready data pipelines, and an AWS-focused deployment strategy. Although the platform runs locally for development, it is designed with a clear migration path to AWS managed services such as Amazon RDS, Amazon MSK, Amazon S3, Amazon EMR, Amazon Glue, Amazon Athena, Amazon MWAA, and Amazon EKS.

The primary objective of this project is to demonstrate how operational healthcare data can be transformed into reliable, analytics-ready datasets while following scalable data engineering and software engineering best practices.

## Business Problem

Healthcare organizations generate large volumes of operational data from patient registrations, appointments, billing systems, insurance claims, and clinical applications. These events originate from multiple services and must be processed reliably to support reporting, operational monitoring, compliance, and business analytics.

Traditional tightly coupled systems make it difficult to scale data processing, integrate new applications, and provide near real-time insights. As organizations grow, they require an event-driven architecture capable of ingesting high-throughput data streams, validating data quality, transforming raw events into trusted datasets, and making curated information available for downstream analytics.

HealthSphere addresses this challenge by implementing a modern data platform based on Apache Kafka, Apache Spark Structured Streaming, Delta Lake, and the Medallion Architecture. The platform separates operational workloads from analytical workloads, improves scalability, promotes data quality, and provides a foundation for cloud-native deployment on AWS.
