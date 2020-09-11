programs = []

# brightness 1 - 254
# color 155 - 453

p = {}
p["name"] = "DOOM Eternal"
p["process_name"] = "DOOMEternalx64vk.exe"
p["color_temperature"] = 454
p["brightness"] = 50
p["priority"] = 5
p["flash"] = False
programs.append(p)

p = {}
p["name"] = "Dark Souls 3"
p["process_name"] = "DarkSoulsIII.exe"
p["color_temperature"] = 454
p["brightness"] = 50
p["priority"] = 4
p["flash"] = False
p["command"] = "taskkill /F /IM dropbox.exe"
programs.append(p)

p = {}
p["name"] = "Clone Hero"
p["process_name"] = "Clone Hero.exe"
p["color_temperature"] = 155
p["priority"] = 6
p["flash"] = True
programs.append(p)

p = {}
p["name"] = "Ori Will Wisps"
p["process_name"] = "oriwotw.exe"
p["color_temperature"] = 153
p["priority"] = 9
p["flash"] = False
programs.append(p)

p = {}
p["name"] = "Dirt Rally"
p["process_name"] = "dirtrally2.exe"
p["color_temperature"] = 250
p["brightness"] = 100
p["priority"] = 15
p["flash"] = False
programs.append(p)

