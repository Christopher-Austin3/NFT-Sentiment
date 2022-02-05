import {Moralis} from "./Moralis";
/* Moralis init code */
const serverUrl = "https://84eaxtbsqopt.usemoralis.com:2053/server";
const appId = "fIWX08dajsrc0PWRwOQrDC6zHvSA8gIfbPh7punG";
Moralis.start({ serverUrl, appId });

/* Authentication code */
async function login() {
  let user = Moralis.User.current();
  if (!user) {
    user = await Moralis.authenticate({ signingMessage: "Log in using Moralis" })
      .then(function (user) {
        console.log("logged in user:", user);
        console.log(user.get("ethAddress"));
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

async function logOut() {
  await Moralis.User.logOut();
  console.log("logged out");
}


function searchNFT(){
  let apes = Moralis.Web3API.token.searchNFTs({q:"ape"})
  console.log(apes)
}

document.getElementById("btn-login").onclick = login;
document.getElementById("btn-logout").onclick = logOut;
document.getElementById("searchnftbutton").onclick = searchNFT;

searchNFT();
