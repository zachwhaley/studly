package com.studly;

import android.app.ListActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;

public class MainActivity extends ListActivity {

	public static final String[] THINGS = {
        "Android",
        "iPhone",
        "WindowsMobile",
        "Blackberry",
        "WebOS",
        "Ubuntu",
        "Windows",
        "Max OS X",
        "Linux",
        "OS/2"
	};

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
				android.R.layout.simple_list_item_1, THINGS);
		setListAdapter(adapter);
	}

}
