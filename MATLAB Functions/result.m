function x = result(answer_scheme_answers, answer_sheet_answers, total_questions)
correctAns = 0;

for i = 1:total_questions
    if (~(answer_sheet_answers(i) == 'X'))
        if (answer_scheme_answers(i) == answer_sheet_answers(i))
            correctAns = correctAns + 1;
        end
    end
end

x = correctAns;
end