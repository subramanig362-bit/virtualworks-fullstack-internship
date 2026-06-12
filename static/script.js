async function saveNote() {

    let note =
    document.getElementById("noteInput").value;

    await fetch("/add_note", {
        method: "POST",
        headers: {
            "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
            content: note
        })
    });

    document.getElementById("noteInput").value = "";

    loadNotes();
}

async function loadNotes() {

    let response =
    await fetch("/notes");

    let notes =
    await response.json();

    let list =
    document.getElementById("notesList");

    list.innerHTML = "";

    notes.forEach(note => {

        let li =
        document.createElement("li");

        li.textContent =
        note.content;

        list.appendChild(li);
    });
}

loadNotes();