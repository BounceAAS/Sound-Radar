extends Node2D

var python_script_path = "main.py"
var file_path = "res://temp/outputs.txt"
var timer: Timer

var transparency_values_DOA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
var transparency_values_loudness = [0.0, 0.0, 0.0, 0.0, 0.0]
var classification = ""
var DL_model = false
var current_help_index = 0

func _ready():
	# Assuming you have 9 ColorRect nodes as children of this node
	get_tree().get_root().set_transparent_background(true)
	
	var screen_size = DisplayServer.screen_get_size()
	DisplayServer.window_set_position(Vector2((screen_size[0]/2 - 550), 0))
	$Help_content.visible = false

# Recursive function to parse the string into a list
func parse_file_list(file_list):
	var DOA_1 = []
	var DOA_2 = []
	var loudness
	var classification
	var num_list = "0123456789"
	
	for i in file_list[0]:
		if i in num_list:
			DOA_1.append(int(i))
	for i in file_list[1]:
		if i in num_list:
			DOA_2.append(int(i))	
	loudness = int(file_list[2])
	classification = file_list[3]
	return [DOA_1, DOA_2, loudness, classification]	
		
func update_score_label(classification):
	# Update the label text with the new score
	$Classification.text = classification

func _on_dl_model_toggled(button_pressed):
	if button_pressed:
		DL_model = true
		print("DL_model on")
	else:
		DL_model = false
		print("DL_model off")
		
func _on_timer_timeout():
	# repeating the tween 
	var tween = get_tree().create_tween()
	tween.tween_property($Scanner, "position", Vector2(1200, 0), 0.95)
	tween.play()
	tween.tween_property($Scanner, "position", Vector2(0, 0), 0)
	
	# Execute the Python script	
	var output = []
	
	if DL_model == true:
		OS.execute("python", [python_script_path, "o", "net"], output)
	else:
		OS.execute("python", [python_script_path], output)
		
	var file = FileAccess.open(file_path, FileAccess.READ)
	var file_list = []
	if file != null:
		while not file.eof_reached():
			var line = file.get_line().strip_edges()  # Remove leading/trailing spaces
			if line != "":
				file_list.append(line)
		file.close()
		print(file_list)
	var info = parse_file_list(file_list)
	# set value of doa rects
	for i in range(9):
		transparency_values_DOA[i] = 0
	for i in info[0]:
		transparency_values_DOA[i] = 1 * float(info[2])/5
	for i in info[1]:
		transparency_values_DOA[i] = 0.5 * float(info[2])/5
	# set value of loudness rects
	for i in range(5):
		transparency_values_loudness[i] = 0
	for i in range(info[2] + 1):
		transparency_values_loudness[i] = 0.5
	classification = info[3]
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	for i in range(9):
		if $Scanner.position[0] > 150 + i * 100:
			var color_rect = get_node("DOA" + str(i + 1))  # Adjust the node names as needed
			color_rect.set_modulate(Color(1, 1, 1, transparency_values_DOA[i]))
		else:
			var color_rect = get_node("DOA" + str(i + 1))  # Adjust the node names as needed
			color_rect.set_modulate(Color(1, 1, 1, 0))
	for i in range(5):
		var color_rect = get_node("Loudness" + str(i))  # Adjust the node names as needed
		color_rect.set_modulate(Color(1, 1, 1, transparency_values_loudness[i]))
	update_score_label(classification)

func _on_help_mouse_entered():
	$Help_content.visible = true
	current_help_index = 0
	$Timer2.start()
	
func _on_help_mouse_exited():
	$Help_content.visible = false

func _on_timer_2_timeout():
	var Cotent = ['This is the SoundRadar.','On the top shows the DOA of sound with the depth','of color indicating the possibilities.', 'On the bottom shows the Loudness of sound in 5 levels.', 'On the right shows classification of sound by DL model.','Check the checkbox "DL model" to enable DL model.','Check the "model" folder in root directory to change','the DL model into your own trained one.','','']
	$Help_content.text = Cotent[current_help_index]
	current_help_index = (current_help_index + 1) % Cotent.size()
