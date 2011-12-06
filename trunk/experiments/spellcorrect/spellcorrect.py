import re, collections
import string

def words(text): return re.findall('[a-z]+', text.lower()) 

replaceable = [
	"aq","yvu", "etcrf", "il", "hn"
];
def exist(l, a):
	for li in l:
		if li == a: return True;
	return False;

def replaceone(word, i, b):
	return [word, word[:i]+b+word[i+1:]];
def replaceperm(word, a, b):
	eidx = [];
	for i in range(len(word)):
		if word[i] == a: eidx.append(i);
	changed = [word];

	for e in eidx:
		for c in changed:
			cr = replaceone(c, e, b);
			for crr in cr:
				if not exist(changed, crr): changed.append(crr);
	return changed;
		

def knownchanges(word_o):
	rword = [word_o];
	for word in rword:
		for r in replaceable:
			for c1 in r:
				for c2 in r:
					for cc in replaceperm(word, c1, c2):
						if (not exist(rword, cc)): rword.append(cc);
	return rword;
	
def edit_distance(a, b):
	total = 0;
	for i in range(min(len(a),len(b))):
		if (a[i] != b[i] ): total += 1;
	
	total += abs(len(a)-len(b));
	return total;

def train(features):
	model = collections.defaultdict(lambda: 1)
	for f in features:
		model[f] += 1;
	return model

NWORDS = train(words(file('corpus.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
	splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	#deletes    = [a + b[1:] for a, b in splits if b]
	#transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
	replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
	#inserts    = [a + c + b     for a, b in splits for c in alphabet]
	rset = set(replaces)
	return rset;
	#return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word_o):
	word_o = word_o.lower();
	
	pl = [];
	for word in knownchanges(word_o):
		print word;
		word = word.lower();
		candidates = known([word]) or known(edits1(word)) or known_edits2(word) or[word]
		pc = max(candidates, key=NWORDS.get);
		if NWORDS.get(pc):
			pl.append(pc)
#		mval = NWORDS.get(macand);

	predictions = [];
	for p in pl:
		exist = False;
		for i in range(len(predictions)):
			if (predictions[i][0] == p):
				predictions[i] = (p,min(edit_distance(p,word_o), predictions[i][1]));
				exist = True;
				break;
		if (not exist):
			predictions.append((p, edit_distance(p,word_o)));
	
	predictions.sort(key=lambda a:a[1]);
	if (len(predictions) > 0 ):
		lowest = predictions[0][1];
		rp = [];
		for p in predictions:
			if p[1] <= lowest: rp.append(p);
			
		return rp;
#	#	return (predictions[len(predictions)-1][0],
	#		predictions[len(predictions)-2][0]);
	else: return None;
		


















