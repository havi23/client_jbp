from ahk import AHK

ahk = AHK(executable_path="drivers/a64.exe")
ahk.run_script('Run Notepad')
win = ahk.find_window(title=b'Untitled - Notepad')
win.send('hello')  # send keys directly to a window (does not need focus!)
win.move(x=200, y=300, width=500, height=800)
win.activate()  # give the window focus
win.disable()  # make the window non-interactable
win.enable()  # enable it again
win.to_top()  # moves window on top of other windows
win.to_bottom()
win.always_on_top = True  # make the windows always on top
win.close()

for window in ahk.windows():
    print(window.title)

#  some more attributes
print(window.text)
print(window.rect)  # (x, y, width, height)
print(window.id)  # ahk_id
print(window.pid)
print(window.process)