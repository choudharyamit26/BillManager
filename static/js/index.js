class Book {
    constructor(product, quantity, price, gst, hsn_code) {
        this.product = product;
        this.quantity = quantity;
        this.price = price;
        this.gst = gst;
        this.hsn_code = hsn_code
    }
}

class Display {
    add(book) {
        let tableBody = document.getElementById('tableBody');
        let uiString = `<tr>
                        <td name='product'>${book.product}</td>
                        <td name='quantity'>${book.quantity}</td>
                        <td name='price' >${book.price}</td>
                        <td name='gst' >${book.gst}</td>
                        <td name='hsn_code'>${book.hsn_code}</td>
                    </tr>`;
        tableBody.innerHTML += uiString;
        // function tableToJSON(table) {
        //     var obj = {};
        //     var row, rows = table.rows;
        //     for (var i=0, iLen=rows.length; i<iLen; i++) {
        //       row = rows[i];
        //       obj[row.cells[0].textContent] = row.cells[1].textContent
        //     }
        //     return JSON.stringify(obj);
        //   }
          
        //   console.log(tableToJSON(document.getElementById('tableBody')));
        
    }

    clear() {
        let libraryForm = document.getElementById('mymodalform');
        libraryForm.reset();
    }
}

// Add submit event listener to libraryForm
let libraryForm = document.getElementById('mymodalform');
libraryForm.addEventListener('button', libraryFormSubmit);

function libraryFormSubmit(e) {
    let product = document.getElementById('product').value;
    let quantity = document.getElementById('quantity').value;
    let price = document.getElementById('price').value;
    let gst = document.getElementById('gst').value;
    let hsn_code = document.getElementById('hsn_code').value;
    let book = new Book(product, quantity, price, gst, hsn_code);
    let display = new Display();
    display.add(book);
    display.clear();
    // e.preventDefault();
}

