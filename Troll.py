import tkinter as tk
from tkinter import messagebox
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt



user_data_filename = "user_data.txt"
sentiments_data_filename = "sentiments_data.txt"

sentiments_list = []

def get_sentiment_rating(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)


    overall_rating = get_sentiment_rating(sentiment_dict['compound'])


    entry = {'message': sentence, 'overall_rating': overall_rating}
    sentiments_list.append(entry)


    with open(sentiments_data_filename, 'a') as file:
        file.write(f"{sentence} | {overall_rating}\n")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Overall sentiment dictionary: {sentiment_dict}\n")
    output_text.insert(tk.END, f"Sentence Overall Rated As: {overall_rating}\n\n")

def load_entries_from_file():

    try:
        with open(sentiments_data_filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                entry_data = line.strip().split(" | ")
                if len(entry_data) == 2:
                    sentiments_list.append({'message': entry_data[0], 'overall_rating': entry_data[1]})
    except FileNotFoundError:
        pass

def analyze_and_display():
    user_input = input_entry.get()
    sentiment_scores(user_input)


    output_text.insert(tk.END, "List of Messages and Overall Ratings:\n")
    for index, entry in enumerate(sentiments_list, start=1):
        output_text.insert(tk.END, f"{index}. Message: {entry['message']}\tOverall Rating: {entry['overall_rating']}\n")

def search_messages():
    search_query = search_entry.get().lower()
    found_entries = [entry for entry in sentiments_list if search_query in entry['message'].lower()]


    output_text.delete(1.0, tk.END)
    if found_entries:
        output_text.insert(tk.END, "Search Results:\n")
        for index, entry in enumerate(found_entries, start=1):
            output_text.insert(tk.END, f"{index}. Message: {entry['message']}\tOverall Rating: {entry['overall_rating']}\n")
    else:
        output_text.insert(tk.END, f"No matching entries found for '{search_query}'.\n")

def plot_sentiment_distribution():
    positive_count = sum(entry['overall_rating'] == 'Positive' for entry in sentiments_list)
    negative_count = sum(entry['overall_rating'] == 'Negative' for entry in sentiments_list)
    neutral_count = sum(entry['overall_rating'] == 'Neutral' for entry in sentiments_list)

    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive_count, negative_count, neutral_count]
    colors = ['green', 'red', 'orange']
    explode = (0.1, 0.1, 0.1)

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    # Display the plot
    plt.title('Sentiment Distribution')
    plt.show()

def remove_entry():
    try:
        index = int(remove_entry_index.get()) - 1
        if 0 <= index < len(sentiments_list):
            del sentiments_list[index]
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Entry removed successfully.\n")
        else:
            messagebox.showerror("Error", "Invalid index.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid index.")


root = tk.Tk()
root.title("Sentiment Analysis Tool")


load_entries_from_file()


input_label = tk.Label(root, text="Enter Your Text:")
input_entry = tk.Entry(root, width=50)
analyze_button = tk.Button(root, text="Analyze", command=analyze_and_display)

search_label = tk.Label(root, text="Search Messages:")
search_entry = tk.Entry(root, width=50)
search_button = tk.Button(root, text="Search", command=search_messages)

output_text = tk.Text(root, width=60, height=20)

plot_button = tk.Button(root, text="Plot Sentiment Distribution", command=plot_sentiment_distribution)

remove_entry_label = tk.Label(root, text="Enter index to remove entry:")
remove_entry_index = tk.Entry(root, width=10)
remove_entry_button = tk.Button(root, text="Remove Entry", command=remove_entry)


input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_entry.grid(row=0, column=1, padx=10, pady=5)
analyze_button.grid(row=0, column=2, padx=10, pady=5)

search_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
search_entry.grid(row=1, column=1, padx=10, pady=5)
search_button.grid(row=1, column=2, padx=10, pady=5)

output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

plot_button.grid(row=3, column=0, columnspan=3, pady=5)

remove_entry_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
remove_entry_index.grid(row=4, column=1, padx=10, pady=5)
remove_entry_button.grid(row=4, column=2, padx=10, pady=5)

  
root.mainloop()
