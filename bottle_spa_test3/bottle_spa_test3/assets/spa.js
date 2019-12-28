;(function(){
    'use strict';
    
    //URLの一覧を配列で用意
    const url_list = [
      'page1',
      'page2',
      'page3',
    ];
    
    function init(){
      $.get('page/page1.html').done((data) => {
          $('.spa').html(data);
      }).fail(() => {
          error();
      });
    }
    
    function hashchange(){
      const page = location.hash.slice(1);
      const in_url = $.inArray(page, url_list);
      if(in_url !== -1){
        $.get(`page/${page}.html`).done((data) => {
          $('.spa').html(data);
        }).fail(() => {
          error();
        });
      }
    }
    
    function error(){
      $('.spa').html('読み込みエラー');
    }
    
    $(window).on("hashchange", () => {
      hashchange();
    });
    
    $(function(){
      init();
    });
    
    })();