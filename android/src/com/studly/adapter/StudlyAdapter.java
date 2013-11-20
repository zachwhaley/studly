package com.studly.adapter;

import com.studly.R;
import com.studly.model.StudlyEvent;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class StudlyAdapter extends ArrayAdapter<StudlyEvent> {
    
    private static final String TAG = "StudlyAdapter";

    public StudlyAdapter(Context context, StudlyEvent.List events) {
        super(context, 0, events);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Log.d(TAG, "Create new view");
        LayoutInflater inflater = (LayoutInflater) getContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View view = inflater.inflate(R.layout.studly_list_item, null);

        StudlyEvent event = getItem(position);
        if (event != null) {
            Log.d(TAG, "creating row for group " + event.getName());
            TextView textView = (TextView) view.findViewById(R.id.row_event);
            textView.setText(event.getName());
        }
        return view;
    }
}
