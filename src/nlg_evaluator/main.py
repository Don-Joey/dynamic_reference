from nltk.translate.bleu_score import corpus_bleu
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score
import bert_score
from .moverscore.moverscore_v2 import get_idf_dict, word_mover_score
#from comet import download_model, load_from_checkpoint
from .BARTScore.bart_score import BARTScorer
from nltk.tokenize import word_tokenize
# Initialize models and scorers
rouge = Rouge()
bert_scorer = bert_score.BERTScorer(lang="en", rescale_with_baseline=True)
#comet_model = load_from_checkpoint(download_model("wmt20-comet-da"))
bart_scorer = BARTScorer(device='cuda', checkpoint='facebook/bart-large-cnn')

# Functions to calculate metrics
from nltk.translate.bleu_score import sentence_bleu
def calculate_bleu(reference_texts_list, candidate_text_list):
    # Tokenize the texts using NLTK's word_tokenize function
    score_list = []
    for reference_texts, candidate_text in zip(reference_texts_list, candidate_text_list):
        reference_tokens = [word_tokenize(ref.lower()) for ref in [reference_texts]]
        candidate_tokens = word_tokenize(candidate_text.lower())
        
        # Calculate BLEU score
        score = sentence_bleu(reference_tokens, candidate_tokens)
        score_list.append(score)
    return score_list

def calculate_rouge_l(references, candidate):
    scores = []
    for cand, ref in zip(references, candidate):
        try:
            score = rouge.get_scores([cand], [ref])
        except:
            score = [{'rouge-l': {'f': 0}}]
        scores.append(score[0]['rouge-l']['f'])
    return scores

def calculate_meteor(references, candidate):
    scores = []
    for ref, cand in zip(references, candidate):
        score = meteor_score([word_tokenize(ref)], word_tokenize(cand))
        scores.append(score)
    return scores

def calculate_bertscore(references, candidate):
    P, R, F1 = bert_scorer.score(candidate, [[ref] for ref in references])
    return F1.tolist()

def calculate_moverscore(references, candidate):
    idf_dict_hyp = get_idf_dict(candidate)  # idf_dict_hyp can be a dummy dictionary
    idf_dict_ref = get_idf_dict(references)
    scores = word_mover_score(references, candidate, idf_dict_ref, idf_dict_hyp, stop_words=[], n_gram=1, remove_subwords=True)
    return scores
'''
def calculate_comet(references, candidate):
    data = [{"src": ref, "mt": candidate} for ref in references]
    return comet_model.predict(data, batch_size=1, gpus=1)
'''
def calculate_bartscore(references, candidate):
    scores = bart_scorer.score(candidate, references)
    return scores

def compute_reference_similarity_score(references, candidate):
    print("begin bleu...")
    bleuscores = calculate_bleu(references, candidate)
    print("begin rouge...")
    rougelscores = calculate_rouge_l(references, candidate)
    print("begin meteor...")
    meteorscores = calculate_meteor(references, candidate)
    print("begin bertscore...")
    bertscores = calculate_bertscore(references, candidate)
    print("begin moverscore...")
    #moverscores = calculate_moverscore(references, candidate)
    moverscores = len(bertscores) * [0.0]
    #print("COMET Score:", calculate_comet(references, candidate))
    print("begin bartscore...")
    bartscores = calculate_bartscore(references, candidate)
    #print("COMET Score:", calculate_comet(references, candidate))
    return bleuscores, rougelscores, meteorscores, bertscores, moverscores, bartscores

# Example usage
if __name__ == "__main__":
    references = ["The cat sits on the mat."]
    candidate = ["A cat is on the mat."]

    print("BLEU Score:", calculate_bleu(references, candidate))
    print("ROUGE-L Score:", calculate_rouge_l(references, candidate))
    print("METEOR Score:", calculate_meteor(references, candidate))
    print("BERTScore:", calculate_bertscore(references, candidate))
    print("MoverScore:", calculate_moverscore(references, candidate))
    #print("COMET Score:", calculate_comet(references, candidate))
    print("BARTScore:", calculate_bartscore(references, candidate))