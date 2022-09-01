import os
import json
import statistics

word_accs = []
char_accs = []
total_cnt = 0
# get ocr accuracy min, max and avg
for root, result_dirs, result_files in os.walk("test"):
    # with open(BASE_DIR+'/appconfig.json', 'r') as myfile:
    # print(root, result_dirs, result_files)
    for result_file in result_files:
        with open(os.path.join(root, result_file), 'r') as file:
            result = file.read()
            result = json.loads(result)
            try:
                word_accs.append(result["ocr_analyse_results"][0]["word_accuracy"])
                char_accs.append(result["ocr_analyse_results"][0]["char_accuracy"])
                total_cnt = total_cnt + result["ocr_analyse_results"][0]["total_words"]
            except:
                continue
print("Word Accuracy")
print("Max: %.2f"% max(word_accs))
print("Min: %.2f"% min(word_accs))
print("Avg: %.2f"% statistics.mean(word_accs))


print("Char Accuracy")
print("Max: %.2f"% max(char_accs))
print("Min: %.2f"% min(char_accs))
print("Avg: %.2f"% statistics.mean(char_accs))

print("Total Words: %d" % total_cnt)