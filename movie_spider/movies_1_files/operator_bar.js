$.extend({renderData:function(e,t,a){a&&(operatable=!0),operatable&&(operatable=!1,$.ajax({url:e,data:t,type:"GET",success:function(e){var n=e.length,s=$(".movie-list-panel.pictext"),i=$(".movie-list-panel.list"),o=s.find(".movie-list-item").length;a&&(s.html(""),i.html(""),o=t.start);for(var l=0;l<n;l++){var r=e[l];s.append($.getPicTextModeContent(r)),i.append($.getListModeContent(r))}"checked"==$("#chkUnwatched").attr("checked")&&$(".watched").hide().siblings(".visible").find(".movie-img").lazyload(),"checked"==$("#chkPlayable").attr("checked")&&$(".unplayable:visible").hide().siblings(".visible").find(".movie-img").lazyload(),$(".movie-list-panel:visible").find(".movie-img:eq("+o+"), .movie-img:gt("+o+")").lazyload({effect:"fadeIn",threshold:100}),$(".list .movie-list-item").mouseenter(function(){navigator.userAgent.toLowerCase().indexOf("msie 7.0")>=0&&$(this).next().next().find(".movie-content .movie-name").hide(),$(this).find(".movie-content-hover").removeClass("scaleY").find(".movie-img-hover").lazyload()}).mouseleave(function(){navigator.userAgent.toLowerCase().indexOf("msie 7.0")>=0&&$(this).next().next().find(".movie-content .movie-name").show(),$(this).find(".movie-content-hover").addClass("scaleY")}),n>0&&(operatable=!0)},error:function(e){a&&$(".movie-list-panel").html("很抱歉，本类型暂无数据... ...").css({"text-align":"center","margin-top":"40px"})}}))},renderDataCount:function(e,t){$.ajax({url:e,data:t,type:"GET",success:function(e){$(".operator-count").html("("+e.total+")"),$(".option-unwatched-count").html("("+e.unwatched_count+")"),$(".option-playable-count").html("("+e.playable_count+")")},error:function(e){}})},getPicTextModeContent:function(e){return e?'<div class="movie-list-item'+(e.is_playable?" playable":" unplayable")+(e.is_watched?" watched":" unwatched")+'"><div class="movie-content"><a href="'+e.url+'" target="_blank"><img data-original="'+e.cover_url+'" class="movie-img" /></a><div class="movie-info"><div class="movie-name"><span class="movie-name-text"><a href="'+e.url+'" target="_blank">'+e.title+"</a></span>"+(e.is_playable?'<span class="playable-sign">[可播放]</span>':"")+'<span class="rank-num">'+e.rank+"</span></div>"+(e.actors.length>0?'<div class="movie-crew">'+e.actors.join(" / ")+"</div>":"")+'<div class="movie-misc">'+(e.release_date.length>0?e.release_date.split("-")[0]+" / ":"")+e.regions.join(" / ")+" / "+e.types.join(" / ")+'</div><div class="movie-rating"><span class="bigstar'+e.rating[1]+'"></span><span class="rating_num">'+e.score+'</span><span class="comment-num">'+e.vote_count+"人评价</span></div></div></div></div>":""},getListModeContent:function(e){return e?'<div class="movie-list-item'+(e.is_playable?" playable":" unplayable")+(e.is_watched?" watched":" unwatched")+'"><div class="movie-content"><div class="movie-name"><span class="movie-name-text"><a href="'+e.url+'" target="_blank">'+e.title+"</a></span>"+(e.is_playable?'<span class="playable-sign">[可播放]</span>':"")+'&nbsp;&nbsp;<span class="rating_num">'+e.score+'</span><span class="comment-num">'+e.vote_count+'人评价</span><span class="rank-num">'+e.rank+'</span></div></div><div class="movie-content-hover scaleY"><a href="'+e.url+'" target="_blank"><img data-original="'+e.cover_url+'" class="movie-img-hover" /></a><div class="movie-info-hover"><div class="movie-name"><span class="movie-name-text"><a href="'+e.url+'" target="_blank">'+e.title+"</a></span>"+(e.is_playable?'<span class="playable-sign">[可播放]</span>':"")+'<span class="rank-num">'+e.rank+"</span></div>"+(e.actors.length>0?'<div class="movie-crew">'+e.actors.join(" / ")+"</div>":"")+'<div class="movie-misc">'+(e.release_date.length>0?e.release_date.split("-")[0]+" / ":"")+e.regions.join(" / ")+" / "+e.types.join(" / ")+'</div><div class="movie-rating-hover"><span class="bigstar'+e.rating[1]+'"></span>  '+e.score+'<span class="comment-num">'+e.vote_count+"人评价</span></div></div></div></div>":""},capture:function(e){e.releaseCapture?e.releaseCapture():window.releaseEvents&&window.releaseEvents(Event.MOUSEMOVE|Event.MOUSEUP)},pageX:function(e){var t=e||window.event;return t.pageX||t.clientX+document.body.scrollLeft-document.body.clientLeft},layerX:function(e){var t=e||window.event;return t.offsetX||t.pageX-$(t.target||t.srcElement).offset().left},throttle:function(e,t){var a;return function(){var n=this,s=arguments;clearTimeout(a),a=setTimeout(function(){t.apply(n,s)},e)}},adjustCursor:function(){var e=$(".cursor");$(e).children().each(function(){var t=$(this);"bigspot"==t.attr("class")?(t.removeClass("bigspot").delay(300).addClass("smallspot"),$(e).width("90px")):(t.removeClass("smallspot").delay(300).addClass("bigspot"),$(e).width("94px"))})}}),$.fn.extend({scaleMark:function(){$("#scale"+$(this).attr("perc")).css("left",$(this).offset().left-$("#opr").offset().left-($("#scale"+$(this).attr("perc")).width()-$(this).width())/2+"px").show()},tooltipShow:function(){var e=$(this),t=e.attr("perc"),a=document.createElement("div");return a.className="tooltip",a.id="ttip"+t,a.innerHTML=t+"%",a.style.left=e.offset().left-$("#opr").offset().left-ttipOffset+"px",$("#opr").append(a),this},tooltipHide:function(){return $("#ttip"+$(this).attr("perc")).remove(),this}});