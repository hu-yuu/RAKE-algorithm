from nltk import sent_tokenize, word_tokenize
from collections import Counter
import re



trstopwords = []
f = open("stopwords.txt","r", encoding='utf-8')
for i in f:
    i= re.sub('[^a-zA-ZÂâğüşöçıİĞÜŞÖÇ]', "", i)
    trstopwords.append(i)
    



class RAKE:
    def __init__(self, stopwords):
        self.stopwords = stopwords

    
    
    def ngrams(self, sentences, n):
        ngrams = []

        for sentence in sentences:
            words = sentence.split()
            for i in range(len(words)-n+1):
                ngrams.append(" ".join(words[i:i+n]))
        return Counter(ngrams)
    
    def delimiterSplit(self, string, n):
        
        wordDelimiters = [r'\b{}\b'.format(word) for word in self.stopwords]
        regexPattern = '|'.join( wordDelimiters) +'|[!.,?:;)(]'
        wds = re.split(regexPattern, string, 0)
        gramList = [word.strip() for word in wds if len(word.split())==n]

        return Counter(gramList)

    

      
    def rake(self, text):
        
        ngram1 = self.delimiterSplit(text, 1)
        ngram2 = self.delimiterSplit(text, 2)
        
        degrees1 = []
        degrees2 = []

        for key, val in ngram1.items():
            deg = 0
            freqs = val
            deg+= val
            for key2, val2 in ngram2.items():
                if key in key2.split():
                    deg += 2
                    freqs += 1
            degrees1.append((key, deg/freqs))

        for key in ngram2.keys():
            score = 0
            w1 = key.split()[0]
            w2 = key.split()[1]
            if w1 in ngram1.keys() :
                score += [score for key,score in degrees1 if key == w1][0]
            else:
                score += 2
            if w2 in ngram1.keys():                
                score += [score for key,score in degrees1 if key == w2][0]
            else:
                score += 2
            degrees2.append((key, score))

        return sorted(degrees1, key=lambda x:x[1], reverse=True), sorted(degrees2, key=lambda x:x[1], reverse=True)


    
if __name__ == '__main__':
    txt = """Oxford English Dictionary (OED) [Oxford İngilizce Sözlüğü]; İngilizceden İngilizceye açıklamalı sözlük. İlk sürümü, A New English Dictionary on Historical Principles'ın (Tarihî Prensiplere Dayanan İngilizce Sözlük) düzeltilmiş ve geliştirilmiş halidir. İlk kez 1 Şubat 1884'te yayımlanmaya başladı. 19 Nisan 1928'e kadar, 12. yüzyıldan günümüze kadar kullanılan İngilizce kelimelerin yer aldığı 10 cilt yayımlandı. 1933'te the New English Dictionary (NED) olan adı Oxford English Dictionary'ye (OED) çevrildi ve 12 cilt artı ilaveler cildi ile birlikte Oxford'daki Clarendon Press tarafından yeniden yayımlandı."""
    kw = RAKE(trstopwords)

    print(kw.rake(txt))


                        
            

