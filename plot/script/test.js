(function() {
  var fn = function() {
    
    (function(root) {
      function now() {
        return new Date();
      }
    
      var force = false;
    
      if (typeof root._bokeh_onload_callbacks === "undefined" || force === true) {
        root._bokeh_onload_callbacks = [];
        root._bokeh_is_loading = undefined;
      }
    
      
      
    
      
      
    
      function run_callbacks() {
        try {
          root._bokeh_onload_callbacks.forEach(function(callback) {
            if (callback != null)
              callback();
          });
        } finally {
          delete root._bokeh_onload_callbacks
        }
        console.debug("Bokeh: all callbacks have finished");
      }
    
      function load_libs(css_urls, js_urls, callback) {
        if (css_urls == null) css_urls = [];
        if (js_urls == null) js_urls = [];
    
        root._bokeh_onload_callbacks.push(callback);
        if (root._bokeh_is_loading > 0) {
          console.debug("Bokeh: BokehJS is being loaded, scheduling callback at", now());
          return null;
        }
        if (js_urls == null || js_urls.length === 0) {
          run_callbacks();
          return null;
        }
        console.debug("Bokeh: BokehJS not loaded, scheduling load and callback at", now());
        root._bokeh_is_loading = css_urls.length + js_urls.length;
    
        function on_load() {
          root._bokeh_is_loading--;
          if (root._bokeh_is_loading === 0) {
            console.debug("Bokeh: all BokehJS libraries/stylesheets loaded");
            run_callbacks()
          }
        }
    
        function on_error() {
          console.error("failed to load " + url);
        }
    
        for (var i = 0; i < css_urls.length; i++) {
          var url = css_urls[i];
          const element = document.createElement("link");
          element.onload = on_load;
          element.onerror = on_error;
          element.rel = "stylesheet";
          element.type = "text/css";
          element.href = url;
          console.debug("Bokeh: injecting link tag for BokehJS stylesheet: ", url);
          document.body.appendChild(element);
        }
    
        for (var i = 0; i < js_urls.length; i++) {
          var url = js_urls[i];
          var element = document.createElement('script');
          element.onload = on_load;
          element.onerror = on_error;
          element.async = false;
          element.src = url;
          console.debug("Bokeh: injecting script tag for BokehJS library: ", url);
          document.head.appendChild(element);
        }
      };var element = document.getElementById("5e72103a-752e-4cf7-8f0c-af3ed3f013ce");
      if (element == null) {
        console.error("Bokeh: ERROR: autoload.js configured with elementid '5e72103a-752e-4cf7-8f0c-af3ed3f013ce' but no matching script tag was found. ")
        return false;
      }
    
      function inject_raw_css(css) {
        const element = document.createElement("style");
        element.appendChild(document.createTextNode(css));
        document.body.appendChild(element);
      }
    
      
      var js_urls = ["https://cdn.pydata.org/bokeh/release/bokeh-1.4.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-widgets-1.4.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-tables-1.4.0.min.js", "https://cdn.pydata.org/bokeh/release/bokeh-gl-1.4.0.min.js"];
      var css_urls = [];
      
    
      var inline_js = [
        function(Bokeh) {
          Bokeh.set_log_level("info");
        },
        
        function(Bokeh) {
          (function() {
            var fn = function() {
              Bokeh.safely(function() {
                (function(root) {
                  function embed_document(root) {
                    
                  var docs_json = '{"87a37ba3-565f-4c4d-a45c-4ce17de32652":{"roots":{"references":[{"attributes":{},"id":"2778","type":"BasicTicker"},{"attributes":{"overlay":{"id":"2812","type":"BoxAnnotation"}},"id":"2785","type":"BoxZoomTool"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"2812","type":"BoxAnnotation"},{"attributes":{"axis_label":"0","bounds":"auto","formatter":{"id":"2801","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","ticker":{"id":"2773","type":"BasicTicker"}},"id":"2772","type":"LinearAxis"},{"attributes":{},"id":"2770","type":"LinearScale"},{"attributes":{},"id":"2794","type":"Selection"},{"attributes":{},"id":"2801","type":"BasicTickFormatter"},{"attributes":{"fill_alpha":{"value":0.2},"fill_color":{"value":"#30a2da"},"line_alpha":{"value":0.2},"line_color":{"value":"#30a2da"},"size":{"units":"screen","value":2.449489742783178},"x":{"field":"0"},"y":{"field":"1"}},"id":"2798","type":"Scatter"},{"attributes":{},"id":"2786","type":"ResetTool"},{"attributes":{"fill_color":{"value":"#30a2da"},"line_color":{"value":"#30a2da"},"size":{"units":"screen","value":2.449489742783178},"x":{"field":"0"},"y":{"field":"1"}},"id":"2796","type":"Scatter"},{"attributes":{"align":null,"below":[{"id":"2772","type":"LinearAxis"}],"center":[{"id":"2776","type":"Grid"},{"id":"2781","type":"Grid"}],"left":[{"id":"2777","type":"LinearAxis"}],"margin":null,"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":300,"renderers":[{"id":"2799","type":"GlyphRenderer"}],"sizing_mode":"fixed","title":{"id":"2764","type":"Title"},"toolbar":{"id":"2787","type":"Toolbar"},"x_range":{"id":"2761","type":"Range1d"},"x_scale":{"id":"2768","type":"LinearScale"},"y_range":{"id":"2762","type":"Range1d"},"y_scale":{"id":"2770","type":"LinearScale"}},"id":"2763","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"2784","type":"WheelZoomTool"},{"attributes":{},"id":"2783","type":"PanTool"},{"attributes":{},"id":"2773","type":"BasicTicker"},{"attributes":{"callback":null,"end":20.823812,"reset_end":20.823812,"reset_start":-29.079832,"start":-29.079832,"tags":[[["0","0",null]]]},"id":"2761","type":"Range1d"},{"attributes":{},"id":"2782","type":"SaveTool"},{"attributes":{"source":{"id":"2793","type":"ColumnDataSource"}},"id":"2800","type":"CDSView"},{"attributes":{"callback":null,"data":{"0":{"__ndarray__":"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","dtype":"float64","shape":[445]},"1":{"__ndarray__":"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","dtype":"float64","shape":[445]}},"selected":{"id":"2794","type":"Selection"},"selection_policy":{"id":"2811","type":"UnionRenderers"}},"id":"2793","type":"ColumnDataSource"},{"attributes":{"text":""},"id":"2764","type":"Title"},{"attributes":{},"id":"2803","type":"BasicTickFormatter"},{"attributes":{"axis_label":"1","bounds":"auto","formatter":{"id":"2803","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","ticker":{"id":"2778","type":"BasicTicker"}},"id":"2777","type":"LinearAxis"},{"attributes":{"dimension":1,"grid_line_color":null,"ticker":{"id":"2778","type":"BasicTicker"}},"id":"2781","type":"Grid"},{"attributes":{},"id":"2811","type":"UnionRenderers"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_multi":null,"active_scroll":"auto","active_tap":"auto","tools":[{"id":"2782","type":"SaveTool"},{"id":"2783","type":"PanTool"},{"id":"2784","type":"WheelZoomTool"},{"id":"2785","type":"BoxZoomTool"},{"id":"2786","type":"ResetTool"}]},"id":"2787","type":"Toolbar"},{"attributes":{},"id":"2768","type":"LinearScale"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#30a2da"},"line_alpha":{"value":0.1},"line_color":{"value":"#30a2da"},"size":{"units":"screen","value":2.449489742783178},"x":{"field":"0"},"y":{"field":"1"}},"id":"2797","type":"Scatter"},{"attributes":{"grid_line_color":null,"ticker":{"id":"2773","type":"BasicTicker"}},"id":"2776","type":"Grid"},{"attributes":{"callback":null,"end":23.081139,"reset_end":23.081139,"reset_start":-18.651464,"start":-18.651464,"tags":[[["1","1",null]]]},"id":"2762","type":"Range1d"},{"attributes":{"data_source":{"id":"2793","type":"ColumnDataSource"},"glyph":{"id":"2796","type":"Scatter"},"hover_glyph":null,"muted_glyph":{"id":"2798","type":"Scatter"},"nonselection_glyph":{"id":"2797","type":"Scatter"},"selection_glyph":null,"view":{"id":"2800","type":"CDSView"}},"id":"2799","type":"GlyphRenderer"}],"root_ids":["2763"]},"title":"Bokeh Application","version":"1.4.0"}}';
                  var render_items = [{"docid":"87a37ba3-565f-4c4d-a45c-4ce17de32652","roots":{"2763":"5e72103a-752e-4cf7-8f0c-af3ed3f013ce"}}];
                  root.Bokeh.embed.embed_items(docs_json, render_items);
                
                  }
                  if (root.Bokeh !== undefined) {
                    embed_document(root);
                  } else {
                    var attempts = 0;
                    var timer = setInterval(function(root) {
                      if (root.Bokeh !== undefined) {
                        clearInterval(timer);
                        embed_document(root);
                      } else {
                        attempts++;
                        if (attempts > 100) {
                          clearInterval(timer);
                          console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                        }
                      }
                    }, 10, root)
                  }
                })(window);
              });
            };
            if (document.readyState != "loading") fn();
            else document.addEventListener("DOMContentLoaded", fn);
          })();
        },
        function(Bokeh) {
        
        
        }
      ];
    
      function run_inline_js() {
        
        for (var i = 0; i < inline_js.length; i++) {
          inline_js[i].call(root, root.Bokeh);
        }
        
      }
    
      if (root._bokeh_is_loading === 0) {
        console.debug("Bokeh: BokehJS loaded, going straight to plotting");
        run_inline_js();
      } else {
        load_libs(css_urls, js_urls, function() {
          console.debug("Bokeh: BokehJS plotting callback run at", now());
          run_inline_js();
        });
      }
    }(window));
  };
  if (document.readyState != "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
})();