var VFCode;

function createCode(from) 
{
 VFCode = "";
 var codeLength = 4; //验证码的长度
 var CodeView = document.getElementById(from);
 var codeChars = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'); //所有候选组成验证码的字符，当然也可以用中文的
 for(var i = 0; i < codeLength; i++) 
 {
  var charNum = Math.floor(Math.random() * 52);
  VFCode += codeChars[charNum];
 }
 if(CodeView) 
 {
  CodeView.className = "VerificationCode";
  CodeView.value = VFCode;
 }

}

function LoginAndRegistWithValidateCode(from,submitName,csrftoken) 
{
 var inputCode=document.getElementById(from).value;
 if(inputCode.length <= 0) 
 {
  alert("请输入验证码！");
 }
 else if(inputCode.toUpperCase() != VFCode.toUpperCase()) 
 {
   alert("验证码输入有误！");
 }
 else 
 {
  if(submitName == 'LoginSubmit'){
    LoginSubmit(csrftoken);
  }else if(submitName == 'RegistSubmit')
    RegistSubmit(csrftoken);
 }    
}

// 加密选项
function CreateCBCOptions(iv){
  return {
    iv: CryptoJS.enc.Utf8.parse(iv),
    mode:CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  };  
}

function encrypt(data,aeskey,cbciv){
    var key = CryptoJS.enc.Utf8.parse(aeskey);
    var secretData = CryptoJS.enc.Utf8.parse(data);
    var encrypted = CryptoJS.AES.encrypt(
    secretData, 
    key, 
    CreateCBCOptions(cbciv)
  );
    return encrypted.toString();
}


function DoEncrypt(keyword,csrftoken,data){
  $.ajaxSettings.async = false;
  var jsonData = new Object();
  $.get('/Param/',{csrfmiddlewaretoken: csrftoken,'KeyWord':keyword},function(result){
    jsonData = JSON.parse(result);
  });
  return encrypt(data,jsonData[0],jsonData[1]);
}

function decrypt(data,aeskey,cbciv){
    var key = CryptoJS.enc.Utf8.parse(aeskey);
    var decrypt = CryptoJS.AES.decrypt(
    data, 
    key, 
    CreateCBCOptions(cbciv)
  );
    return CryptoJS.enc.Utf8.stringify(decrypt).toString();
}



function BlackListOperation(opreration,userid,csrftoken){
  $.post('/BlackListOperation/',{'Operation':opreration,csrfmiddlewaretoken: csrftoken,'UserID':userid},function(status){
    if (status == 'login'){
      document.getElementById('loginbutton').click();
    }else if(status == 'add'){
      alert('已屏蔽');
      location.reload();
    }else if(status == 'delete'){
      alert('已取消屏蔽');
      location.reload();
    }else if(status == 'login'){
      document.getElementById('loginbutton').click();
    }else{
      alert(status);
    }
  })
}

function GetNotificationInfo(){
  var PushNotificationslist = document.getElementById('PushNotifications-list');
  if(PushNotificationslist){
    while(PushNotificationslist.hasChildNodes()){
      PushNotificationslist.removeChild(PushNotificationslist.firstChild);
    }
  }  
  $.get('/Notice/',{},function(returndata){
    if (returndata == 'login'){
      document.getElementById('loginbutton').click();  
    }else{
      var jsonData = JSON.parse(returndata)
      for (var i=0;i<jsonData.length;i++){
        var NTDiv = document.createElement('div');
        NTDiv.setAttribute('class', 'PushNotifications-item PushNotifications-newItem');
        NTDiv.setAttribute('style', 'font-size:14px;width:363px;background:#ffffff;border-bottom:1px solid  #EBEBEB;text-overflow:ellipsis; white-space:nowrap; overflow:hidden;');
        NTDiv.setAttribute('id', jsonData[i].ID);

        var NTUser = document.createElement('a');
        NTUser.setAttribute('href', '/UserProfile/Topic/'+ jsonData[i].SourceUserID +'/LE/1/');
        NTUser.setAttribute('style', 'text-decoration:none;');
        NTUser.innerText = jsonData[i].SourceUserNick + ' ';

        var NTDefualt = document.createElement('span');
        NTDefualt.innerText = ' ' + jsonData[i].Connector + ' '

        var NTTopic = document.createElement('a');
        NTTopic.setAttribute('href', "javascript:RemoveNotificationInfo('one','"+ jsonData[i].ID +"','"+ jsonData[i].TargetURL +"')");
        NTTopic.setAttribute('style', 'text-decoration:none;');
        NTTopic.setAttribute('title', jsonData[i].Title);
        NTTopic.innerText = jsonData[i].Title;

        NTDiv.appendChild(NTUser);
        NTDiv.appendChild(NTDefualt);
        NTDiv.appendChild(NTTopic);

        PushNotificationslist.appendChild(NTDiv);

      }
    }
  })
}

function RemoveNotificationInfo(method, ID, TargetUrl){
  if (method == 'one'){
    window.location.href=TargetUrl;
    var NotificationCountNode = document.getElementById('NotificationCount');
    if (NotificationCountNode){
      NotificationCountNode.parentNode.removeChild(NotificationCountNode);
    }
    $.ajax({type:'delete',url:'/Notice/',data:{'IDs':ID}});
  }else{
    var ID_Array = [];
    var PushNotificationslist = document.getElementById('PushNotifications-list');
    while(PushNotificationslist.hasChildNodes()){
      if (PushNotificationslist.firstChild.getAttribute('id')){
        ID_Array.push(PushNotificationslist.firstChild.getAttribute('id'));
        PushNotificationslist.removeChild(PushNotificationslist.firstChild);
      }else{
        PushNotificationslist.removeChild(PushNotificationslist.firstChild);
      }
    }
    IDs = ID_Array.join(',');
    $.ajax({type:'delete',url:'/NotificationInfo/',data:{'IDs':IDs}});
    var NotificationCountNode = document.getElementById('NotificationCount');
    if (NotificationCountNode){
      NotificationCountNode.parentNode.removeChild(NotificationCountNode);
    }
    document.getElementById('PushNotificationsClose').click();
  }
}

function TickDiv(){
  var url = window.location.href;
  var AnchorID = url.split("/")[8];
  if (AnchorID != 'Share') {
    document.getElementById(AnchorID).setAttribute('style', 'border:2px solid  #FABCBA;');
    window.scrollTo({top:document.getElementById(AnchorID).offsetTop,behavior:"smooth"});
  }
}

function CommentConversation(url,csrftoken,ObjectID,replayuser,replayeduser,from){
  $.post(url,{csrfmiddlewaretoken: csrftoken,'ObjectID':ObjectID,'replayuser':replayuser,'replayeduser':replayeduser,'from':from},function(status){})
}

function SpecialTopicFollow(url,csrftoken,SpecialTopicID){
  $.post(url,{csrfmiddlewaretoken: csrftoken,'SpecialTopicID':SpecialTopicID},function(status){
    if(status == 'follow'){
      alert('关注成功!');
      location.reload();
    }else if(status == 'login'){
      document.getElementById('loginbutton').click();      
    }else if(status == 'cancel'){
      alert('取消关注!');
      location.reload();
    }
  })  
}

function Circusee(url,FilterWord){
  $.get(url,{'RollCallID':FilterWord},function(status){
    if(status == 'collect'){
      alert('收藏成功!');
    }else if(status == 'login'){
      document.getElementById('loginbutton').click();      
    }else{
      alert(status);
    }
  })
}

function RollCallReplay(url,csrftoken,FilterWord){
  var RollCallReplayContent=document.getElementById('RollCallReplayTextArea').value;
  var Chk_RollCallReplayContent = RollCallReplayContent.replace(/(^s*)|(s*$)/g, "").length;
  if(Chk_RollCallReplayContent != 0){
    if(Chk_RollCallReplayContent < 10){
      alert('观点不能少于10个字符！')
    }else{
      if(Chk_RollCallReplayContent > 50){
        alert('观点不能多于50个字符!')
      }else{
        $.post(url,{csrfmiddlewaretoken: csrftoken,'RollCallReplayContent':RollCallReplayContent,'FilterWord':FilterWord},function(status){
          if(status=='replayok'){
            alert('回复成功！');
            location.reload();
          }else{
            alert(status);
          }           
        })
      }
    }
  }else{
    alert('请输入观点!')
  }
}

function PublishRollCall(csrftoken){
  var RollCallTitle = document.getElementById('RollCallTitle').value;
  var TargetUserNick = document.getElementById('TargetUserNick').value;
  var RollCallContent = document.getElementById('RollCallContent').value;
  var Chk_RollCallTitle = RollCallTitle.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_TargetUserNick = TargetUserNick.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_RollCallContent = RollCallContent.replace(/(^s*)|(s*$)/g, "").length; 
  if(Chk_RollCallTitle !=0 && Chk_TargetUserNick !=0  &&  Chk_RollCallContent!=0){
    if(Chk_RollCallContent>30){
      alert('发表观点不能超过30个字符!');
    }else{
    $.post('/PublishRollCall/',{csrfmiddlewaretoken: csrftoken,'RollCallTitle':RollCallTitle,'TargetUserNick':TargetUserNick,'RollCallContent':RollCallContent},function(status){
      if(status=='publishok'){
        alert('发布成功！');
        location.reload();
      }else if(status=='login'){
        document.getElementById('EssayPublishBoardCancel').click();
        document.getElementById('loginbutton').click();
      }else if(status=='titleisexisted'){
        alert('点名标题内容已存在！');
      }else{
        alert(status);
      }      
    });}
  }else{
    alert('请完整输入必要栏目！');
  }
}

function Replay(csrftoken,ParentID,Type){
  var ObjectID = document.getElementById("ObjectContent").getAttribute('ObjectID');
  if (ParentID){
    var ContentObject = document.getElementById('Replaybox#' + ParentID);    
  }else{
    var ContentObject = document.getElementById('CommentTextArea');
  }
 
  var Content = ContentObject.value;
  var Chk_Content = Content.replace(/(^s*)|(s*$)/g, "").length;
  if(Chk_Content!=0){
    $.post('/Replay/',{'Type':Type,csrfmiddlewaretoken: csrftoken,'ObjectID':ObjectID,'ParentID':ParentID,'Content':Content},function(status){
      if(status=='replayok'){
        alert('回复成功！');
        location.reload();
      }else if(status=='login'){
        document.getElementById('loginbutton').click();
      }
    });    
  }else{
    alert('没有回复内容！');
    CommentObject.focus();
  }
}

function HideReplayBox(changeSuffix,removeSuffix,csrftoken,ParentID,from){
  document.getElementById(ParentID+changeSuffix).setAttribute('onclick', "javascript:ShowReplayBox(this,'" + csrftoken + "','" + ParentID + "','" + from + "')")
  var parentDIV = document.getElementById(ParentID);
  parentDIV.removeChild(document.getElementById(ParentID + removeSuffix))
}

function ShowReplayBox(obj,csrftoken,ParentID,from){
  obj.setAttribute('onclick', "javascript:HideReplayBox('#replayBtn','#replayDiv','" + csrftoken + "','"+ ParentID +"','" + from + "')");

  var replayDiv = document.createElement('div');
  replayDiv.setAttribute('style', 'margin-top:8px;');
  replayDiv.setAttribute('id', ParentID+'#replayDiv');
  var replaybox = document.createElement("textarea");
  replaybox.setAttribute('class', 'replaybox');
  replaybox.setAttribute('id', 'Replaybox#' + ParentID);
  replayDiv.appendChild(replaybox);

  var replaybuttonDiv = document.createElement('div');
  replaybuttonDiv.setAttribute('style', 'margin-top:5px;')  
  var replaybutton = document.createElement("button");
  replaybutton.setAttribute('class', 'Button Button--primary Button--blue');
  replaybutton.innerText='确定';
  replaybutton.setAttribute('style', 'height:30px;width:70px;font-size:10px;margin-right:8px;')
  replaybutton.setAttribute('onclick', "javascript:Replay('" + csrftoken + "','" + ParentID +"','" + from + "')");
  var replaycancel = document.createElement("button");
  replaycancel.setAttribute('class', 'Button Button--primary');
  replaycancel.innerText='取消';
  replaycancel.setAttribute('style', 'height:30px;width:70px;font-size:10px;');
  replaycancel.setAttribute('onclick', "javascript:HideReplayBox('#replayBtn','#replayDiv','" + csrftoken + "','"+ ParentID +"','" + from + "')");

  var parent = document.getElementById(ParentID);
  replaybuttonDiv.appendChild(replaybutton);
  replaybuttonDiv.appendChild(replaycancel);
  replayDiv.appendChild(replaybuttonDiv);
  
  parent.appendChild(replayDiv);
}


var TipOffObjectID;
var TipOffType;
function OpenTipOffView(ObjectID, Type){
  TipOffObjectID = ObjectID;
  TipOffType = Type;
}


function TipOff(csrftoken){
  var content = document.getElementById('TipOffContent').value;
  $.post('/TipOff/',{csrfmiddlewaretoken: csrftoken,'TopicID':TipOffObjectID,'Type':TipOffType, 'Content':content},function(status){
                if(status=='success'){
                  alert('已收到您的投诉!');
                  location.reload();
                }else if(status=='cancel'){
                  alert('重复举报!');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              });  
}

function Collect(ObjectID, csrftoken, Type){
  $.post('/Collect/',{csrfmiddlewaretoken: csrftoken,'ObjectID':ObjectID,'Type':Type},function(status){
                if(status=='Collect'){
                  alert('已收藏');
                  location.reload();
                }else if(status=='CollectCancel'){
                  alert('已取消收藏');
                  location.reload();
                }else if(status=='Concern'){
                  alert('已关注');
                  location.reload();
                }else if(status=='ConcernCancel'){
                  alert('已取消关注');
                  location.reload();
                }else if(status=='Circusee'){
                  alert('已围观');
                  location.reload();
                }else if(status=='CircuseeCancel'){
                  alert('已取消围观');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              });  
}

function UserCollect(url,csrftoken,ArticleID){
  var CollectButton = document.getElementById('CollectButton');
  CollectButton.disabled='disabled';
  $.post(url,{csrfmiddlewaretoken: csrftoken,'ArticleID':ArticleID
              },function(status){
                if(status=='collect'){
                  alert('已收藏');
                  location.reload();
                }else if(status=='cancel'){
                  alert('已取消收藏');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              }
        )
  setTimeout(function(){CollectButton.disabled='';},1000);
}

function UserLink(url,csrftoken,userid,operation){
  var LinkButton = document.getElementById('LinkButton');
  LinkButton.disabled='disabled';
  $.post(url,{csrfmiddlewaretoken: csrftoken,
              'UserID':userid,'Operation':operation
              },function(status){
                if(status=='add'){
                  alert('已关注');
                  window.location.reload();
                }else if(status=='delete'){
                  alert('已取消关注');
                  window.location.reload();
                }else if(status=='login'){
                  document.getElementById('loginbutton').click();
                }else{
                  alert(status);
                }
              }
        )
  setTimeout(function(){LinkButton.disabled='';},1000);
}

function UserProfileUpdate(url,csrftoken){
  var UserImageData = document.getElementById('UserImageChangeShow').src;
  var UserImageFormat = document.getElementById('UserImageChangeInput').value.split('.')[1];
  var UserNickName = document.getElementById('UserProfileNickName').value;
  var UserDescription = document.getElementById('UserProfileDescription').value;
  var UserSex = document.getElementById('UserProfileSexOptions').value;
  var UserConstellation = document.getElementById('UserProfileConstellation').value;
  var UserEmail = document.getElementById('UserProfileemail').value;
  var UserRegion = document.getElementById('UserProfileRegion').value;

  var Chk_UserNickName = UserNickName.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserDescription = UserDescription.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserSex = UserSex.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserConstellation = UserConstellation.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserEmail = UserEmail.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserRegion = UserRegion.replace(/(^s*)|(s*$)/g, "").length;
  if(Chk_UserNickName !=0 && Chk_UserDescription !=0 && Chk_UserSex !=0 && Chk_UserConstellation !=0 && Chk_UserEmail !=0 && Chk_UserRegion !=0){
    $.post(url,{csrfmiddlewaretoken: csrftoken,
                'UserImageData':UserImageData,
                'UserImageFormat':UserImageFormat,
                'UserNickName':UserNickName,
                'UserDescription':UserDescription,
                'UserSex':UserSex,
                'UserConstellation':UserConstellation,
                'UserEmail':UserEmail,
                'UserRegion':UserRegion,
              },function(status){
                if(status=='Nick'){
                  alert('昵称已经存在!');
                }else if(status=='success'){
                  location.reload();
                  alert('修改成功!');
                }else if(status=='invariant'){
                  alert('基础信息修改成功!')
                }else{
                  alert(status)
                }
              })

  }else{
    alert('必要信息不能为空！')
  }
}

function JumpToPage(mainurl,InputID,anchor){
  var PageNum = document.getElementById(InputID).value;
  window.location.href=mainurl+PageNum+'#'+anchor;
}


function QRcodeShare(URL){
  if(document.getElementById("QRcodeBoard").getAttribute('class')=='modal fade'){
    document.getElementById("qrcode").innerHTML = "";
  }
  var DomainName="http://www.nagetive.com"
  var qrcode = new QRCode(document.getElementById("qrcode"), {width : 200,height : 200});
  var elText = DomainName + URL;
  qrcode.makeCode(elText);
}

function clearQRcodeDivHtml(){
  document.getElementById("qrcode").innerHTML = "";
}

function AttitudeOperate(Type,ObjectID,Point,csrftoken) {
  var VoteBtn = document.getElementById('Button' + Point + '#' + ObjectID);
  VoteBtn.disabled = 'disabled';
  $.post('/AttitudeOperate/',{csrfmiddlewaretoken: csrftoken,'Type':Type,'ObjectID':ObjectID,'Point':Point},function(status){
    if(status == ('Cancel')){
      document.getElementById('Button' + Point + '#' + ObjectID).setAttribute('class','Button VoteButton VoteButton--up')
      document.getElementById('Span' + Point + '#' + ObjectID).innerText = String(parseInt(document.getElementById('Span' + Point + '#' + ObjectID).innerText) - 1)
    }else if(status == ('Become')){
      document.getElementById('Button' + Point + '#' + ObjectID).setAttribute('class','Button VoteButton VoteButton--up is-active')
      document.getElementById('Button' + String(Math.abs(parseInt(Point)-1)) + '#' + ObjectID).setAttribute('class','Button VoteButton VoteButton--up')
      document.getElementById('Span' + Point + '#' + ObjectID).innerText = String(parseInt(document.getElementById('Span' + Point + '#' + ObjectID).innerText) + 1)
      document.getElementById('Span' + String(Math.abs(parseInt(Point)-1)) + '#' + ObjectID).innerText = String(parseInt(document.getElementById('Span' + String(Math.abs(parseInt(Point)-1)) + '#' + ObjectID).innerText) - 1)
    }else if(status == ('Confirm')){
      document.getElementById('Button' + Point + '#' + ObjectID).setAttribute('class','Button VoteButton VoteButton--up is-active')
      document.getElementById('Span' + Point + '#' + ObjectID).innerText = String(parseInt(document.getElementById('Span' + Point + '#' + ObjectID).innerText) + 1)      
    }else if(status == ('login')){
      document.getElementById('loginbutton').click();
    }
  })
  setTimeout(function(){VoteBtn.disabled='';},500);
}


function PublishTopic(object,type,csrftoken)
{   
    object.innerText = '发布中...';
    var TopicID = (type == 'Edit' ? document.getElementById('Topic' + type + 'ID').value : '');
    var Title = document.getElementById('Topic' + type + 'Title').value;
    var Category = document.getElementById('Topic' + type + 'Category').options[document.getElementById('Topic' + type + 'Category').selectedIndex].text;
    var Content = eval('CKEDITOR.instances.Topic' + type + 'TextArea.getData()');
    var Description = eval('CKEDITOR.instances.Topic' + type + 'TextArea.document.getBody().getText().substring(0,140)');
    var Themes = document.getElementById('Topic' + type + 'Themes').value;

    if(Title.replace(/(^s*)|(s*$)/g, "").length !=0 
       && Content.replace(/(^s*)|(s*$)/g, "").length !=0 
       && Description.replace(/(^s*)|(s*$)/g, "").length !=0 
       && Themes.replace(/(^s*)|(s*$)/g, "").length !=0)
    {
      $.post('/PublishTopic/',{csrfmiddlewaretoken: csrftoken,
                               'TopicID':TopicID,
                               'Title':Title,
                               'Category':Category,
                               'Content':Content,
                               'Description':Description,
                               'Themes':Themes},function(status){
                                                 object.innerText = '发  布';
                                                 if(status=='ok'){
                                                   alert('发布成功!');
                                                   location.reload();
                                                 }else if(status=='login'){
                                                   alert('还未登录!');
                                                 }else {
                                                   alert(status);
                                                 }
                                               });
    }else{
      alert('请完整输入必要栏目!');
    }
}


function FetchTopic(TopicID, csrftoken)
{
  $.post('/FetchTopic/', {'TopicID':TopicID, csrfmiddlewaretoken: csrftoken}, function(result){
    var FetchInfo = JSON.parse(result);
    if (FetchInfo){
      document.getElementById('TopicEditTitle').value = FetchInfo.Title;
      var opts = document.getElementById("TopicEditCategory");
      for(var i=0;i<opts.options.length;i++){
        if(FetchInfo.Category==opts.options[i].value){
          opts.options[i].selected = 'selected';
        }
      }
      CKEDITOR.instances.TopicEditTextArea.setData(FetchInfo.Content);
      document.getElementById('TopicEditThemes').value = FetchInfo.Themes;
      document.getElementById('TopicEditID').value = FetchInfo.TopicID;
    }
  }) 
}



function ClickButton(id)
{
    document.getElementById(id).click();
}

function Comment(url, csrftoken, type)
{   var ContentObject = document.getElementById("CommentTextArea")
    var Comment = ContentObject.value;
    var Chk_Content = Comment.replace(/(^s*)|(s*$)/g, "").length;
    var TopicID = document.getElementById("TopicContent").getAttribute('TopicID');

    if(Chk_Content!=0){
      $.post(url, {'Type':type, csrfmiddlewaretoken: csrftoken, 'Comment':Comment, 'TopicID':TopicID}, function(status){
        if(status == 'ok'){
          alert('评论成功!');
          location.reload();
        }else{
          ClickButton('loginbutton');
        }
      }
      );  
    }else{
      alert('没有输入评论内容!');
      ContentObject.focus();
    }
    
}

function LoginSubmit(csrftoken)
{   
    var username = DoEncrypt('SecretKey',csrftoken,document.getElementById('loginusername').value);
    var password = DoEncrypt('SecretKey',csrftoken,document.getElementById('loginpassword').value);
    $.post('/login/',{csrfmiddlewaretoken: csrftoken,'username':username,'password':password},function(status)
      {if(status)
        {alert('登录成功!');
        location.reload();
      }else{
        alert('用户名或密码错误！');
      }
    });
}

function Logout(url)
{
   $.get(url,function(status){
    if(status == 'Logout'){
      location.reload();
    }
   })
}

function RegistSubmit(csrftoken)
{
    var userimagedata = document.getElementById('UserImageShow').src;
    var format = document.getElementById('UserImageInput').value;
    var userimageformat = format.split('.')[1];
    var username = DoEncrypt('SecretKey',csrftoken,document.getElementById('registusername').value);
    var usernickname = DoEncrypt('SecretKey',csrftoken,document.getElementById('registusernickname').value);
    var password = DoEncrypt('SecretKey',csrftoken,document.getElementById('registpassword').value);
    var email = DoEncrypt('SecretKey',csrftoken,document.getElementById('registemail').value);
    $.post('/regist/',{csrfmiddlewaretoken: csrftoken,'userimagedata':userimagedata,'userimageformat':userimageformat,'username':username,'usernickname':usernickname,'password':password,'email':email},function(status)
      {if(status=='ok'){
        alert('注册成功!');
        location.reload();
      }else{
        alert(status);
      }
    });
}

function Search(source)
{
  var SearchValue = document.getElementById('SearchInput').value;
  var SearchSelect = document.getElementById('SearchSelect');
  var SearchPart = SearchSelect.options[SearchSelect.selectedIndex].title
  location.href='/Search/' + SearchPart + '/' + SearchValue + '/LE/1';
}

function CloseTopic(obj)
{
    var TopicID = obj.getAttribute("name");
    var TopicDIV = document.getElementById(TopicID);
    if(TopicDIV){
        TopicDIV.parentNode.removeChild(TopicDIV);
    }
}

function UploadImg(target,source)
{
    document.getElementById(target).setAttribute('data-source', source);
    document.getElementById(target).click();
}

function UploadUserImg(obj) {
  var file = obj.files[0];    
  console.log(obj);console.log(file);
  console.log("file.size = " + file.size);
  var reader = new FileReader();
  reader.onloadstart = function (e) {
     console.log("开始读取....");
  }
    reader.onprogress = function (e) {
         console.log("正在读取中....");
  }
  reader.onabort = function (e) {
     console.log("中断读取....");
  }
  reader.onerror = function (e) {
      console.log("读取异常....");
  }
  reader.onload = function (e) {
      console.log("成功读取....");
  var img = document.getElementById(obj.getAttribute('data-source'));
      dataformat = e.target.result.split(';', 1)[0]
      if(dataformat == 'data:image/png' || dataformat == 'data:image/jpeg'){
        img.src = e.target.result;
      }else{
        alert('图片格式必须为png或者jpg!');
      }
      //img.src = e.target.result;
      //alert(img.src);
   //或者 img.src = this.result;  //e.target == this
  }
      reader.readAsDataURL(file);
  }
  function EssayPublish(){
    alert('发布')
  }