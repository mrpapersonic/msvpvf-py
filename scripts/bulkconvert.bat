for %%i in (*.veg) do (
	python3 msvpvf.py -i "%%i" --version 13 --type veg
)
pause