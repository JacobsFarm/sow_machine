@echo off
rem Starts the local server and opens the control page in Edge (Web Serial needs Chrome or Edge).
cd /d "%~dp0"
start "" msedge http://localhost:8080
node server.js
