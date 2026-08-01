@echo off
git remote remove origin 2>nul
git remote add origin https://github.com/harys-rifai/traceroute-git-phyton.git
git branch -M main
git push -u origin main
