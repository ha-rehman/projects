//function myAxios(method, url, body=null){
//  return new Promise((resolve, reject)=> {
//      const xhr = new XMLHttpRequest();
//      xhr.open(method, url);
//      xhr.responseType = 'json';
//
//      xhr.setRequestHeader('Content-Type', 'application/json');
//
//      xhr.onload = () => {
//
//          if (xhr.status >= 400){
//              reject(xhr.response);
//              // console.log('Failed!!');
//          } else {
//              resolve(xhr.response);
//              // console.log(xhr.response);
//          }
//      }
//      xhr.onerror = () => {
//          reject(xhr.response);
//          // console.log('Error!!!');
//      }
//
//
//      xhr.send(JSON.stringify(body));
//  })
//}
//
//
//
//
//
//
//const url = '/question';
//
//
//// myAxios('GET', url);
//
//myAxios('POST', url, {name: 'Hello'}).then((res) => {
//  console.log(res.name);
//}).catch((err) => {
//
//});
//
//
//
//
//




function getBotResponse(input) {
return new Promise((resolve,reject)=>(
//paste here

fetch('question', {method: "POST", body: JSON.stringify({input: input})}).then(res => res.text()).then(res => {

var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
	  var text1=res.replace(exp, "<a target= '_blank' href='$1'>$1</a>");

resolve(text1)}).catch(reject)
) )

}