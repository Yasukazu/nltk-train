    function startRecognition() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'ja-JP';
        recognition.interimResults = false;

        recognition.onstart = function() {
            document.getElementById('result').innerText = '音声認識中...';
        };

        recognition.onresult = function(event) {
            if (event.results.length > 0 && event.results[0].isFinal) {
                // 最終結果が得られた場合
                console.log(event.results);
                const transcript = event.results[0][0].transcript;
                const confidence = event.results[0][0].confidence;
                document.getElementById('confidence').innerText = '確証度: ' + confidence;
                document.getElementById('transcript').value = transcript;
                document.getElementById('result').innerText = '音声認識成功!';
                // ここで認識結果をサーバーに送信することができます
                /*
                fetch("get_trans", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: transcript })
                })
                .then(res => res.json())
                .then(data => {
                    const reply = data.reply || data.error || "（応答エラー）";
                    document.getElementById('result').innerText += '\nBot: ' + reply;
                    speak(reply);
                })
                .catch(err => {
                    document.getElementById('result').innerText += '\n（サーバーエラー）';
                    console.error(err);
                }); */
            }
            else if (event.results.length === 0 && event.results[0].isFinal) {
                console.error("No speech-recognized value!");
                document.getElementById('result').innerText = '音声認識結果がありません!';
            }
            else if (event.results.length > 0 && event.results[0].isFinal === false) {
                // 中間結果を表示
                const interimTranscript = event.results[0][0].transcript;
                document.getElementById('result').innerText = `認識中:{event.results.length}:{interimTranscript}`;
            }
            // 認識結果をテキストエリアに表示
            document.getElementById('transcript').value = event.results[0][0].transcript;
        };
        recognition.onerror = function(event) {
            document.getElementById('result').innerText = '音声認識エラー: ' + event.error;

            
        };

        recognition.onend = function() {
            document.getElementById('result').innerText += '\n音声認識終了';
        };
        recognition.start();
    }
    function speak(text) {
        const audio = new Audio();
        fetch("chatbot-proxy.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.blob())
        .then(blob => {
            audio.src = URL.createObjectURL(blob);
            audio.play();
        })
        .catch(err => console.error("音声取得エラー:", err));
    }
    // 音声認識のサポートを確認
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        console.log("音声認識に対応しています。");
    } else {
        console.log("音声認識に対応していません。");
    }
    // {url_for('static',filename='js/script.js')}}