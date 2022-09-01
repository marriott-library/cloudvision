import ocr_analyse_test
import os
import pandas as pd
import statistics

with open(os.path.join("original_tsv", "export.tsv"), encoding="utf8") as file:
    df = pd.read_csv(file, delimiter="\t")
    df = df[df['ocr_t'].notnull()].loc[:,df.columns == 'ocr_t']
    ocrs =(df.values)



word_accs = []
char_accs = []
total_cnt = 0


for ocr in ocrs:
    ocr_analyse_results = ocr_analyse_test.analysis_ocr_from_txts(ocr)
    # print(ocr_analyse_results)
    word_accs.append(ocr_analyse_results[0]["word_accuracy"])
    char_accs.append(ocr_analyse_results[0]["char_accuracy"])
    total_cnt = total_cnt + ocr_analyse_results[0]["total_words"]


print("Word Accuracy")
print("Max: %.2f"% max(word_accs))
print("Min: %.2f"% min(word_accs))
print("Avg: %.2f"% statistics.mean(word_accs))


print("Char Accuracy")
print("Max: %.2f"% max(char_accs))
print("Min: %.2f"% min(char_accs))
print("Avg: %.2f"% statistics.mean(char_accs))

print("Total Words: %d" % total_cnt)