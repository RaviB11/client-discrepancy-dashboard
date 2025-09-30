**Client Data Discrepancy Dashboard**

This project simulates a critical client-facing tool designed to transparently identify and report on data migration errors during a system implementation. 
It automates the data validation process by programmatically comparing pre- and post-migration datasets.

The core of the project is a Python script that leverages the Pandas library to execute advanced comparison logic (mimicking SQL's FULL OUTER JOIN). 
It identifies specific discrepancies, such as value mismatches, missing records, or new records, and compiles them into a clean, structured CSV report.

This final report serves as a direct data source for a business intelligence tool like Tableau, enabling the creation of a clear, actionable dashboard. 
The goal is to transform a complex technical validation process into a collaborative and transparent experience for the client, significantly reducing the need for manual checks.
