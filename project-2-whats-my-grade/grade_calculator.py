def calculate_grade_and_final_needed():
    print("--- APPLIED MACHINE LEARNING: GRADE CALCULATOR ---\n")

    # 1. INPUT YOUR DATA
    homework_scores = [85, 90, 70, 88, 95]
    quiz_scores = [80, 85, 60, 90]
    midterm_score = 72
    target_grade = 80.0

    # Base Weights
    hw_weight = 0.30
    quiz_weight = 0.20
    midterm_weight = 0.20
    final_weight = 0.30

    # 2. CALCULATE HOMEWORK (Drop lowest)
    # Sort scores, drop the last one (which is the lowest if sorted ascending, 
    # but wait, sorted() is ascending, so [-1] is highest. Let's use [:-1] after sorting ascending to drop the lowest)
    hw_sorted = sorted(homework_scores)
    hw_dropped_lowest = hw_sorted[1:] # Keep everything except the first (lowest) score
    hw_average = sum(hw_dropped_lowest) / len(hw_dropped_lowest)
    hw_points = hw_average * hw_weight
    
    print(f"HOMEWORK:")
    print(f" -> Scores: {homework_scores}")
    print(f" -> Dropped lowest ({min(homework_scores)}). Kept: {hw_dropped_lowest}")
    print(f" -> Average: {hw_average:.2f} | Weighted Points: {hw_points:.2f}\n")

    # 3. CALCULATE QUIZZES (Drop lowest)
    quiz_sorted = sorted(quiz_scores)
    quiz_dropped_lowest = quiz_sorted[1:] 
    quiz_average = sum(quiz_dropped_lowest) / len(quiz_dropped_lowest)
    quiz_points = quiz_average * quiz_weight
    
    print(f"QUIZZES:")
    print(f" -> Scores: {quiz_scores}")
    print(f" -> Dropped lowest ({min(quiz_scores)}). Kept: {quiz_dropped_lowest}")
    print(f" -> Average: {quiz_average:.2f} | Weighted Points: {quiz_points:.2f}\n")

    # 4. CALCULATE MIDTERM & CHECK SPECIAL RULE
    print(f"MIDTERM & SPECIAL RULE CHECK:")
    if midterm_score < 50:
        print(f" -> Midterm score is {midterm_score} (Below 50).")
        print(f" -> SPECIAL RULE TRIGGERED: Midterm becomes 0%, Final Exam becomes 50%.")
        midterm_points = 0
        final_weight = 0.50 # Update final weight
    else:
        print(f" -> Midterm score is {midterm_score} (Above 50). Standard rules apply.")
        midterm_points = midterm_score * midterm_weight
        
    print(f" -> Midterm Weighted Points: {midterm_points:.2f}\n")

    # 5. CALCULATE CURRENT STANDING
    current_points = hw_points + quiz_points + midterm_points
    
    print(f"CURRENT STANDING:")
    print(f" -> Total Points Earned So Far: {current_points:.2f} / 70.00 possible")
    print(f" -> Current Course Grade (if Final was 0): {current_points:.2f}%\n")

    # 6. CALCULATE REQUIRED FINAL EXAM SCORE
    points_needed = target_grade - current_points
    required_final_score = points_needed / final_weight
    
    print(f"TARGET: {target_grade}%")
    print(f" -> Points still needed: {points_needed:.2f}")
    print(f" -> Final Exam Weight: {final_weight * 100:.0f}%")
    
    if required_final_score > 100:
        print(f" -> REQUIRED FINAL SCORE: {required_final_score:.2f}% (Impossible! Max is 100%)")
        print(f" -> Conclusion: You cannot reach your target grade.")
    elif required_final_score < 0:
        print(f" -> REQUIRED FINAL SCORE: 0% (You have already secured your target grade!)")
    else:
        print(f" -> REQUIRED FINAL SCORE: {required_final_score:.2f}%")
        print(f" -> Conclusion: You need to score at least a {required_final_score:.2f} on the Final Exam to get a {target_grade}%.")

if __name__ == "__main__":
    calculate_grade_and_final_needed()