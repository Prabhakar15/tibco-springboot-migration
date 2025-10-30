package com.loan.hexagonal.domain.model;

public class CreditScore {
    
    private int score;
    private String rating;

    public CreditScore(int score) {
        this.score = score;
        this.rating = calculateRating(score);
    }

    private String calculateRating(int score) {
        if (score >= 750) return "EXCELLENT";
        if (score >= 700) return "GOOD";
        if (score >= 650) return "FAIR";
        if (score >= 600) return "POOR";
        return "VERY_POOR";
    }

    public int getScore() { return score; }
    public String getRating() { return rating; }
}
