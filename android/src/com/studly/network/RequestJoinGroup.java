package com.studly.network;

import com.octo.android.robospice.request.retrofit.RetrofitSpiceRequest;
import com.studly.model.StudlyGroup;

public class RequestJoinGroup extends RetrofitSpiceRequest<String, StudlyApi> {

    private StudlyGroup mEvent;
    private String mEmail;
    private boolean mJoin;

    public RequestJoinGroup(StudlyGroup event, String email, boolean join) {
        super(String.class, StudlyApi.class);
        mEvent = event;
        mEmail = email;
        mJoin = join;
    }

    @Override
    public String loadDataFromNetwork() throws Exception {
        //return getService().joinGroup(mEvent.getName(), mEmail, Boolean.toString(mJoin));
        return "OK";
    }

}
