function inComma(inputNum){
    var tagId;

    if(inputNum == 1){
        tagId = document.getElementById("money");
    } else if(inputNum == 2){
        tagId = document.getElementById("mo");
    }

    var input = tagId.value;

    if(input.match(/[０-９]/g)){
        input = input.replace(/[０-９]/g, function(s) {
            return String.fromCharCode(s.charCodeAt(0) - 0xFEE0);
        });
    } else if(input.match(/[^0-9,]/g)){
        alert("数字で入力してください");
        tagId.value = "";
        return;
    }

    input = input.replace(/[^0-9]/g, "");
    inAns = input.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');

    if(inAns.match(/[^0-9]/g)){
        tagId.value = inAns;
    }
}

function clearText(el){
    var targetId;

    if(el == 1){
        targetId = document.getElementById("money");
    } else if(el == 2){
        targetId = document.getElementById("mo");
    }

    targetId.value = "";
}

function checkValue(el){
    var money;
    var category;
    var formName;

    if(el == 1){
        money = document.getElementById("money");
        formName = document.budgetForm;
    } else if(el == 2){
        money = document.getElementById("mo");
        category = document.getElementById("category");
        formName = document.spendingForm;
    }

    if(money.value.length == 0){
        alert("金額を入力してください");
        return;
    } else if(el == 2 && category.value.length == 0){
        alert("カテゴリーを選択してください");
        return;
    }

    money.value = money.value.replace(/[^0-9]/g, "");
    formName.submit();
}