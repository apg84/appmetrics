{
  "variables": {
    "srcdir%": "./src",
    "nandir%": "./node_modules/nan",
    'build_id%': '.<!(["python", "./generate_build_id.py"])',
    'appmetricsversion%':  '<!(["python", "./get_from_json.py", "./package.json", "version"])',
  },
  "conditions": [
    ['OS=="aix"', {
      "variables": {
        "SHARED_LIB_SUFFIX": ".a",
      },
    }],
  ],

  "target_defaults": {
    "cflags_cc!": [ '-fno-exceptions' ],
    "include_dirs": [ '<(srcdir)', '<(nandir)'],
    "target_conditions": [
      ['_type=="shared_library"', {
        'product_prefix': '<(SHARED_LIB_PREFIX)',
        "conditions": [
          ['OS=="aix"', {
            'product_extension': 'a',
          },{
          }],
        ],
      }],
    ],
    "conditions": [
      ['OS=="aix"', {
        "defines": [ "_AIX", "AIX" ],
        "libraries": [ "-Wl,-bexpall,-brtllib,-G,-bernotok,-brtl" ],
      }],
      ['OS=="mac"', {
        "defines": [ "__MACH__", "__APPLE__",  ],
         "libraries": [ "-undefined dynamic_lookup" ],
      }],
      ['OS=="linux"', {
        "defines": [ "_LINUX", "LINUX" ],
      }],
      ['OS=="win"', {
        "defines": [ "_WINDOWS", "WINDOWS"  ],
        "libraries": [ "Ws2_32" ],
        "msvs_settings": {
          "VCCLCompilerTool": {
            "AdditionalOptions": [
              "/EHsc",
              "/MD",
            ]
          },
        },
      }]
    ],
  },

  "targets": [
      {
      "target_name": "appmetrics",
      "sources": [
        "<(INTERMEDIATE_DIR)/appmetrics.cpp",
      ],
      'variables': {
        'appmetricslevel%':'<(appmetricsversion)<(build_id)',
      },
      'actions': [{
        'action_name': 'Set appmetrics reported version/build level',
        'inputs': [ "<(srcdir)/appmetrics.cpp" ],
        'outputs': [ "<(INTERMEDIATE_DIR)/appmetrics.cpp" ],
        'action': [
          'python',
          './replace_in_file.py',
          '<(srcdir)/appmetrics.cpp',
          '<(INTERMEDIATE_DIR)/appmetrics.cpp',
          '--from="99\.99\.99\.29991231"',
          '--to="<(appmetricslevel)"',
          '-v'
         ],
      }],
    },
    {
      "target_name": "nodeenvplugin",
      "type": "shared_library",
      "sources": [
        "<(srcdir)/plugins/node/env/nodeenvplugin.cpp",
      ],
    },
    {
      "target_name": "nodeprofplugin",
      "type": "shared_library",
      "sources": [
        "<(srcdir)/plugins/node/prof/nodeprofplugin.cpp",
      ],
    },
    {
      "target_name": "nodegcplugin",
      "type": "shared_library",
      "sources": [
        "<(srcdir)/plugins/node/gc/nodegcplugin.cpp",
      ],
    },

    {
      "target_name": "install",
      "type": "none",
      "dependencies": [
        "appmetrics",
        "nodeenvplugin",
        "nodegcplugin",
        "nodeprofplugin",
     ],
      "copies": [
        {
          "destination": "./",
          "files": [
            "<(PRODUCT_DIR)/appmetrics.node",
          ],
        },
        {
          "destination": "./plugins",
          "files": [
            "<(PRODUCT_DIR)/<(SHARED_LIB_PREFIX)nodeenvplugin<(SHARED_LIB_SUFFIX)",
            "<(PRODUCT_DIR)/<(SHARED_LIB_PREFIX)nodegcplugin<(SHARED_LIB_SUFFIX)",
            "<(PRODUCT_DIR)/<(SHARED_LIB_PREFIX)nodeprofplugin<(SHARED_LIB_SUFFIX)",
          ],
        },
      ],
    },
  ],
}

