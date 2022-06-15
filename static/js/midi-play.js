let input = document.getElementById('input');

input.addEventListener('submit', () => {
    console.log('読み込んだ!');
    var t = document.getElementById('text').value;
    console.log(t)
    alert('ファイルを読み込みました！');
});

console.log('あああ')