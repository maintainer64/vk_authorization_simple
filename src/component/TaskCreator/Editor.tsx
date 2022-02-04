enum ExerciseType{
    Input,
    Checkbox,
    Radio
}

interface ExerciseAnswer{
    content: string;
    checked: boolean;
}

interface ExerciseItem{
    task: string;
    answers: [];
    type: ExerciseType;
}

export function Editor(){

}