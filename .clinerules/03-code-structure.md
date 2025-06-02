# Code Structure Standards

This document outlines standards for code structure and organization in the ProAGI project.

- Organize tests mirroring the application code structure. (Ref: 09-testing.md)
- Use structured logging (JSON format) with mandatory context fields (`timestamp`, `level`, `component_name`, `traceId`, `appId`, `requestId`). (Ref: 01-core-framework.md section 5)
