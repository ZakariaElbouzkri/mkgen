mkdir -p ~/mkgen
cp -p ./script.py ~/mkgen/script.py
echo 'alias mkgen="python3 ~/mkgen/script.py"' >> ~/.zshrc
echo 'alias mkgen="python3 ~/mkgen/script.py"' >> ~/.bashrc
echo "\033[1;32mInstalation Done"
echo "open new terminal and try: mkgen [file_extention(.c/.cpp)]"