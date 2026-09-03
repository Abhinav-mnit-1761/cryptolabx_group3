#ifndef SUBSTITUTION_H
#define SUBSTITUTION_H


#include <string>
using namespace std;

string encrypt(const string& plaintext, const string& key);
string decrypt(const string& ciphertext, const string& key);
void frequency_analysis(const string& ciphertext);
void word_frequency_analysis(const string& ciphertext);
void pattern_analysis(const string& ciphertext);
string apply_substitution(const string& ciphertext, const string& key);
void display_partial_plaintext(const string& plaintext);
bool valid_substitution(const string& key, char cipher_letter, char plain_letter);
string frequency_substitution(const string& ciphertext);
bool verify_solution(const string& plaintext,
                     const string& ciphertext,
                     const string& key);

#endif
