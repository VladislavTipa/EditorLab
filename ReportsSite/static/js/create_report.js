const container = document.getElementById('sections-container');
const orderInput = document.getElementById('sections-order');

function updateOrder() {
    const sections = Array.from(container.children);
    const order = sections.map(section => section.dataset.type);
    orderInput.value = JSON.stringify(order);
}

document.getElementById('add-text').addEventListener('click', () => {
    const textSection = document.createElement('div');
    textSection.classList.add('dynamic-section');
    textSection.setAttribute('data-type', 'text');
    textSection.innerHTML = `
        <textarea name="sections_text[]" placeholder="Введите текст"></textarea>
        <button type="button" class="remove-section">Удалить</button>
    `;
    container.appendChild(textSection);
    addRemoveFunctionality(textSection);
    updateOrder();
});

document.getElementById('add-image').addEventListener('click', () => {
    const imageSection = document.createElement('div');
    imageSection.classList.add('dynamic-section');
    imageSection.setAttribute('data-type', 'image');
    imageSection.innerHTML = `
        <input type="file" name="sections_image[]" accept="image/*">
        <input type="text" name="sections_image_caption[]" placeholder="Подпись к изображению">
        <button type="button" class="remove-section">Удалить</button>
    `;
    container.appendChild(imageSection);
    addRemoveFunctionality(imageSection);
    updateOrder();
});

document.getElementById('add-code').addEventListener('click', () => {
    const codeSection = document.createElement('div');
    codeSection.classList.add('dynamic-section');
    codeSection.setAttribute('data-type', 'code');
    codeSection.innerHTML = `
        <textarea name="sections_code[]" placeholder="Введите код"></textarea>
        <button type="button" class="remove-section">Удалить</button>
    `;
    container.appendChild(codeSection);
    addRemoveFunctionality(codeSection);
    updateOrder();
});

function addRemoveFunctionality(section) {
    section.querySelector('.remove-section').addEventListener('click', () => {
        section.remove();
        updateOrder();
    });
}
