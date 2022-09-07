from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


file = open('speech.txt',mode='r', encoding='utf-8')
speech = file.read()
file.close()

wordcloud = WordCloud(max_font_size=50, background_color="white").generate(speech)

plt.figure(facecolor = None)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()
