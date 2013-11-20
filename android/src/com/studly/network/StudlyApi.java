package com.studly.network;

import retrofit.http.Field;
import retrofit.http.FormUrlEncoded;
import retrofit.http.GET;
import retrofit.http.POST;

import com.studly.model.StudlyEvent;

public interface StudlyApi {

    @GET("/todo")
    StudlyEvent.List getEvents();

    @FormUrlEncoded
    @POST("/todo")
    String joinGroup(@Field("event") String event,
                     @Field("email") String email,
                     @Field("join") String join);
}
